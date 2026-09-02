"""Exhaustively compare every bundled tag with every semantic category.

This is a development-only audit tool.  BubbleLens never loads the embedding
model at runtime.  The output keeps the full decision trail so low-confidence
or disputed moves can be inspected before a precomputed map is released.
"""

from __future__ import annotations

import argparse
import ast
import csv
import gzip
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

import server
from taxonomy import EXACT_OVERRIDES, TAXONOMY, classify_tag


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tags_enhanced.csv"
MODEL_NAME = "intfloat/multilingual-e5-small"
MODEL_SLUG = MODEL_NAME.replace("/", "--")
CACHE_DIR = ROOT / ".audit-cache"
OUTPUT_DIR = ROOT / "audit_output"
SPECIAL_FOLDERS = {"copyright", "character", "other"}
SOURCE_FOLDERS = {"3": "copyright", "4": "character"}


@dataclass(frozen=True)
class CategorySpec:
    folder_id: str
    folder_name: str
    folder_description: str
    category_id: str
    category_name: str

    @property
    def key(self) -> tuple[str, str]:
        return self.folder_id, self.category_id

    @property
    def label(self) -> str:
        return f"{self.folder_name} / {self.category_name}"

    @property
    def passage(self) -> str:
        return (
            "passage: 这是一个绘图提示词分类。"
            f"大分类是“{self.folder_name}”，定义为“{self.folder_description}”；"
            f"细分类是“{self.category_name}”。标签应主要描述{self.category_name}，"
            f"并属于{self.folder_name}的范围。"
        )


def normalized(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    return array / np.maximum(norms, 1e-12)


def data_fingerprint() -> str:
    digest = hashlib.sha256()
    with DATA_FILE.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    digest.update(str(server.TAG_ALIAS_OVERRIDES).encode("utf-8"))
    return digest.hexdigest()[:20]


def tag_text(tag: dict, prefix: str = "query") -> str:
    aliases = "、".join(dict.fromkeys(tag.get("aliases") or []))
    wiki = " ".join((tag.get("wiki") or "").split())
    return (
        f"{prefix}: 绘图提示词 {tag['name'].replace('_', ' ')}。"
        f"中文名称：{tag.get('cn', '')}。别名：{aliases}。"
        f"定义与用法：{wiki}"
    )


def semantic_categories() -> list[CategorySpec]:
    result = []
    for folder in TAXONOMY:
        if folder["id"] in SPECIAL_FOLDERS:
            continue
        for category in folder["categories"]:
            result.append(CategorySpec(
                folder["id"], folder["name"], folder["description"],
                category["id"], category["name"],
            ))
    return result


def current_locations(catalog: dict) -> dict[str, tuple[str, str]]:
    return {
        tag["name"]: (folder["id"], category["id"])
        for folder in catalog["folders"]
        for category in folder["categories"]
        for tag in category["tags"]
    }


def encode_tags(model: SentenceTransformer, tags: list[dict], fingerprint: str) -> np.ndarray:
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / f"{MODEL_SLUG}-{fingerprint}-tags.npy"
    if path.exists():
        cached = np.load(path)
        if cached.shape[0] == len(tags):
            print(f"Using cached tag embeddings: {cached.shape}", flush=True)
            return cached
    print(f"Encoding all {len(tags):,} tag definitions...", flush=True)
    embeddings = model.encode(
        [tag_text(tag) for tag in tags], batch_size=128,
        normalize_embeddings=True, show_progress_bar=True,
    ).astype(np.float32)
    np.save(path, embeddings)
    return embeddings


def build_prototypes(
    model: SentenceTransformer,
    tags: list[dict],
    embeddings: np.ndarray,
    categories: list[CategorySpec],
    locations: dict[str, tuple[str, str]],
    seed_count: int,
) -> np.ndarray:
    """Blend human-readable category definitions with representative members."""
    category_index = {item.key: index for index, item in enumerate(categories)}
    members: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, tag in enumerate(tags):
        location = locations[tag["name"]]
        if location in category_index:
            members[location].append(index)

    base = model.encode(
        [item.passage for item in categories], batch_size=128,
        normalize_embeddings=True, show_progress_bar=False,
    ).astype(np.float32)
    prototypes = base.copy()
    for category_position, item in enumerate(categories):
        candidates = sorted(
            members[item.key], key=lambda index: (-tags[index]["count"], tags[index]["name"]),
        )[:seed_count]
        if not candidates:
            continue
        # The definition remains the anchor; members add vocabulary and concrete
        # examples without allowing one popular tag to define an entire class.
        centroid = embeddings[candidates].mean(axis=0)
        prototypes[category_position] = 0.48 * base[category_position] + 0.52 * centroid
    return normalized(prototypes).astype(np.float32)


def read_anchor_expectations() -> dict[str, tuple[str, str]]:
    tree = ast.parse((ROOT / "test_taxonomy.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "expected" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    return {}


def confidence_label(similarity: float, margin: float, current_rank: int | None) -> str:
    if similarity >= 0.79 and margin >= 0.055 and (current_rank is None or current_rank <= 3):
        return "high"
    if similarity >= 0.70 and margin >= 0.022:
        return "medium"
    return "low"


def nearest_category_evidence(
    tags: list[dict],
    embeddings: np.ndarray,
    locations: dict[str, tuple[str, str]],
    category_index: dict[tuple[str, str], int],
    neighbor_count: int,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Exact k-NN over all known general tags; no approximate search is used."""
    training = [
        index for index, tag in enumerate(tags)
        if locations[tag["name"]] in category_index
    ]
    queries = [
        index for index, tag in enumerate(tags)
        if locations[tag["name"]][0] not in {"copyright", "character"}
    ]
    training_embeddings = embeddings[training]
    training_classes = np.array(
        [category_index[locations[tags[index]["name"]]] for index in training], dtype=np.int32,
    )
    training_position = {tag_index: position for position, tag_index in enumerate(training)}
    vote_scores = np.zeros((len(tags), len(category_index)), dtype=np.float32)
    consensus = np.zeros(len(tags), dtype=np.float32)
    examples = [""] * len(tags)
    print(
        f"Exact neighbor comparisons={len(queries) * len(training):,} "
        f"({len(queries):,} queries x {len(training):,} known tags)", flush=True,
    )
    for start in range(0, len(queries), 256):
        batch = queries[start : start + 256]
        similarities = embeddings[batch] @ training_embeddings.T
        for row, tag_index in enumerate(batch):
            own_position = training_position.get(tag_index)
            if own_position is not None:
                similarities[row, own_position] = -1.0
        nearest = np.argpartition(similarities, -neighbor_count, axis=1)[:, -neighbor_count:]
        nearest = np.take_along_axis(
            nearest,
            np.argsort(np.take_along_axis(similarities, nearest, axis=1), axis=1)[:, ::-1],
            axis=1,
        )
        for row, tag_index in enumerate(batch):
            neighbor_positions = nearest[row]
            neighbor_similarities = similarities[row, neighbor_positions]
            # Squared excess similarity lets genuinely close definitions dominate
            # while weak, generic neighbors contribute very little.
            weights = np.maximum(neighbor_similarities - 0.60, 0.001) ** 2
            classes = training_classes[neighbor_positions]
            for class_index, weight in zip(classes, weights):
                vote_scores[tag_index, class_index] += float(weight)
            total = float(vote_scores[tag_index].sum())
            if total:
                vote_scores[tag_index] /= total
                consensus[tag_index] = float(vote_scores[tag_index].max())
            examples[tag_index] = " | ".join(
                f"{tags[training[int(position)]]['name']}={score:.4f}"
                for position, score in zip(neighbor_positions[:5], neighbor_similarities[:5])
            )
    return vote_scores, consensus, examples


def audit(args: argparse.Namespace) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    tags = server.read_tags()
    # Always rebuild the reference labels from the deterministic taxonomy.
    # Loading last run's generated map here would create circular self-training
    # and amplify a mistaken assignment on every subsequent pass.
    locations = {tag["name"]: classify_tag(tag) for tag in tags}
    categories = semantic_categories()
    category_index = {item.key: index for index, item in enumerate(categories)}
    human_locations = dict(EXACT_OVERRIDES)
    human_locations.update(read_anchor_expectations())
    folder_indexes: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(categories):
        folder_indexes[item.folder_id].append(index)

    print(
        f"Tags={len(tags):,}; semantic categories={len(categories):,}; "
        f"pairwise comparisons={len(tags) * len(categories):,}", flush=True,
    )
    model = SentenceTransformer(MODEL_NAME)
    embeddings = encode_tags(model, tags, data_fingerprint())
    prototypes = build_prototypes(
        model, tags, embeddings, categories, locations, args.seed_count,
    )

    # This is the deliberately exhaustive step: every tag vector is multiplied
    # by every semantic category vector, with no search shortcut or shortlist.
    semantic_scores = embeddings @ prototypes.T
    adjusted_scores = semantic_scores.copy()
    neighbor_scores, neighbor_consensus, neighbor_examples = nearest_category_evidence(
        tags, embeddings, locations, category_index, args.neighbor_count,
    )
    adjusted_scores += args.neighbor_prior * neighbor_scores
    for row, tag in enumerate(tags):
        current = locations[tag["name"]]
        exact_position = category_index.get(human_locations.get(tag["name"]))
        if exact_position is not None:
            # Human wiki-level decisions target their declared destination,
            # never whichever generated map happened to be loaded previously.
            adjusted_scores[row, exact_position] += args.exact_prior
            continue
        current_position = category_index.get(current)
        if current_position is None:
            continue
        adjusted_scores[row, folder_indexes[current[0]]] += args.folder_prior
        adjusted_scores[row, current_position] += args.current_prior

    top_count = min(5, len(categories))
    top_indexes = np.argpartition(adjusted_scores, -top_count, axis=1)[:, -top_count:]
    top_indexes = np.take_along_axis(
        top_indexes,
        np.argsort(np.take_along_axis(adjusted_scores, top_indexes, axis=1), axis=1)[:, ::-1],
        axis=1,
    )

    records = []
    assignments = {}
    changed = 0
    confidence_counts = defaultdict(int)
    for row, tag in enumerate(tags):
        current = locations[tag["name"]]
        semantic_order = np.argsort(semantic_scores[row])[-top_count:][::-1]
        semantic_best = categories[int(semantic_order[0])]

        if current[0] in {"copyright", "character"}:
            # Danbooru source type is stronger evidence than lexical similarity.
            # Letter subcategories are deterministic navigation, not semantics.
            proposed = current
            confidence = "authoritative"
            margin = 1.0
            current_rank = 1
            method = "source-type-and-initial"
        else:
            first = int(top_indexes[row, 0])
            second = int(top_indexes[row, 1])
            proposed_spec = categories[first]
            proposed = proposed_spec.key
            margin = float(adjusted_scores[row, first] - adjusted_scores[row, second])
            current_position = category_index.get(current)
            current_rank = None
            if current_position is not None:
                current_score = adjusted_scores[row, current_position]
                current_rank = int(np.count_nonzero(adjusted_scores[row] > current_score) + 1)
            confidence = confidence_label(float(semantic_scores[row, first]), margin, current_rank)
            method = "definition-all-category-comparison"

        neighbor_position = int(np.argmax(neighbor_scores[row]))
        neighbor_best = categories[neighbor_position]

        if proposed != current:
            changed += 1
        confidence_counts[confidence] += 1
        assignments[tag["name"]] = list(proposed)
        candidate_text = " | ".join(
            f"{categories[int(position)].label}={adjusted_scores[row, int(position)]:.4f}"
            for position in top_indexes[row]
        )
        records.append({
            "tag": tag["name"],
            "cn": tag.get("cn", ""),
            "source_type": tag["category"],
            "wiki": " ".join((tag.get("wiki") or "").split()),
            "current_folder": current[0],
            "current_category": current[1],
            "semantic_best_folder": semantic_best.folder_id,
            "semantic_best_category": semantic_best.category_id,
            "neighbor_best_folder": neighbor_best.folder_id,
            "neighbor_best_category": neighbor_best.category_id,
            "neighbor_consensus": f"{neighbor_consensus[row]:.6f}",
            "nearest_examples": neighbor_examples[row],
            "proposed_folder": proposed[0],
            "proposed_category": proposed[1],
            "changed": int(proposed != current),
            "confidence": confidence,
            "semantic_similarity": f"{semantic_scores[row, category_index[proposed]]:.6f}"
                if proposed in category_index else "",
            "margin": f"{margin:.6f}",
            "current_rank": current_rank,
            "method": method,
            "top_candidates": candidate_text,
        })

    fieldnames = list(records[0])
    full_path = OUTPUT_DIR / "semantic_full_audit.csv"
    with full_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    changes = sorted(
        (item for item in records if item["changed"]),
        key=lambda item: ({"low": 0, "medium": 1, "high": 2}.get(item["confidence"], 3),
                          float(item["margin"])),
    )
    with (OUTPUT_DIR / "semantic_changes.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(changes)

    anchors = read_anchor_expectations()
    anchor_correct = sum(tuple(assignments.get(name, ())) == expected for name, expected in anchors.items())
    summary = {
        "model": MODEL_NAME,
        "databaseFingerprint": data_fingerprint(),
        "tagCount": len(tags),
        "semanticCategoryCount": len(categories),
        "pairwiseComparisonCount": len(tags) * len(categories),
        "changedCount": changed,
        "confidenceCounts": dict(confidence_counts),
        "anchorCorrect": anchor_correct,
        "anchorTotal": len(anchors),
        "anchorAccuracy": anchor_correct / len(anchors) if anchors else None,
        "currentPrior": args.current_prior,
        "exactPrior": args.exact_prior,
        "folderPrior": args.folder_prior,
        "seedCount": args.seed_count,
        "neighborCount": args.neighbor_count,
        "neighborPrior": args.neighbor_prior,
    }
    (OUTPUT_DIR / "semantic_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    if args.write_map:
        payload = {
            "databaseFingerprint": data_fingerprint(),
            "model": MODEL_NAME,
            "assignments": assignments,
        }
        with gzip.open(ROOT / "data" / "semantic_tag_locations.json.gz", "wt", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"Full audit: {full_path}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-count", type=int, default=24)
    parser.add_argument("--current-prior", type=float, default=0.035)
    parser.add_argument("--exact-prior", type=float, default=1.0)
    parser.add_argument("--folder-prior", type=float, default=0.008)
    parser.add_argument("--neighbor-count", type=int, default=15)
    parser.add_argument("--neighbor-prior", type=float, default=0.025)
    parser.add_argument("--write-map", action="store_true")
    audit(parser.parse_args())


if __name__ == "__main__":
    main()
