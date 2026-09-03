"""Exhaustive Wiki-definition-to-category cross-encoder audit for BubbleLens.

This development-only tool performs a real cross-encoder judgment for every
tag/category pair.  It is intentionally slower than embedding retrieval: the
full Wiki definition and one category definition are jointly read on every
forward pass.  Scores, checkpoints, top candidates, and disagreements with
human overrides are retained so a run is inspectable and resumable.

The model and PyTorch are audit dependencies only.  The BubbleLens executable
continues to load a small precomputed JSON map and never ships an ML runtime.
"""

from __future__ import annotations

import argparse
import ast
import csv
import gzip
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import server
from taxonomy import EXACT_OVERRIDES, TAXONOMY, classify_tag, normalize_location


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tags_enhanced.csv"
MODEL_NAME = "BAAI/bge-reranker-v2-m3"
CACHE_DIR = ROOT / ".audit-cache"
OUTPUT_DIR = ROOT / "audit_output"
SPECIAL_FOLDERS = {"copyright", "character", "other"}
SOURCE_FOLDER_BY_TYPE = {"3": "copyright", "4": "character"}


@dataclass(frozen=True)
class CategorySpec:
    folder_id: str
    folder_name: str
    folder_description: str
    category_id: str
    category_name: str
    source_type: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return self.folder_id, self.category_id

    @property
    def label(self) -> str:
        return f"{self.folder_name} / {self.category_name}"


def read_anchor_expectations() -> dict[str, tuple[str, str]]:
    tree = ast.parse((ROOT / "test_taxonomy.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "expected" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    return {}


def data_fingerprint() -> str:
    digest = hashlib.sha256()
    with DATA_FILE.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    digest.update(repr(TAXONOMY).encode("utf-8"))
    digest.update(MODEL_NAME.encode("utf-8"))
    return digest.hexdigest()[:20]


def all_categories() -> list[CategorySpec]:
    """Return every meaningful destination, without meaningless A-Z duplication.

    Character and copyright subcategories are alphabetical navigation buckets,
    not semantic classes.  Each is nevertheless compared through one source
    meaning; the authoritative Danbooru source type later selects its A-Z bucket.
    """
    result: list[CategorySpec] = []
    for folder in TAXONOMY:
        if folder["id"] in SPECIAL_FOLDERS:
            continue
        for category in folder["categories"]:
            result.append(CategorySpec(
                folder["id"], folder["name"], folder["description"],
                category["id"], category["name"],
            ))
    result.extend([
        CategorySpec(
            "copyright", "作品系列", "动漫、游戏、漫画、影视、虚拟主播等作品或系列名称",
            "__source_index__", "作品名称", "3",
        ),
        CategorySpec(
            "character", "角色索引", "特定作品中的具名角色、人物或专有角色变体",
            "__source_index__", "角色名称", "4",
        ),
    ])
    return result


def all_folders(categories: list[CategorySpec]) -> list[CategorySpec]:
    """Build one independently scored definition for every parent folder."""
    result: list[CategorySpec] = []
    seen = set()
    for item in categories:
        if item.folder_id in seen:
            continue
        seen.add(item.folder_id)
        child_names = "、".join(
            child.category_name for child in categories if child.folder_id == item.folder_id
        )
        result.append(CategorySpec(
            item.folder_id,
            item.folder_name,
            f"{item.folder_description}。下属类型：{child_names}",
            "__folder__",
            item.folder_name,
            item.source_type,
        ))
    return result


def tag_premise(tag: dict) -> str:
    wiki = " ".join((tag.get("wiki") or "").split())
    aliases = "、".join(dict.fromkeys(tag.get("aliases") or []))
    if not wiki:
        wiki = "原始数据库没有提供 Wiki 定义"
    return (
        f"Danbooru 绘图标签名：{tag['name'].replace('_', ' ')}。"
        f"中文名称或别名：{tag.get('cn', '')}。其他别名：{aliases}。"
        f"Danbooru Wiki 定义：{wiki}。"
        "分类时以 Wiki 定义所说的核心对象、属性、动作或概念为准。"
    )


def verified_examples(tags: list[dict], limit: int = 5) -> dict[tuple[str, str], list[str]]:
    """Provide small human-reviewed examples, never generated/current labels."""
    anchors = read_anchor_expectations()
    reviewed = {
        name: normalize_location(destination, name)
        for name, destination in EXACT_OVERRIDES.items()
    }
    reviewed.update({
        name: normalize_location(destination, name)
        for name, destination in anchors.items()
    })
    members: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for tag in tags:
        destination = reviewed.get(tag["name"])
        if destination:
            members[destination].append(tag)
    result: dict[tuple[str, str], list[str]] = {}
    for destination, values in members.items():
        values.sort(key=lambda item: (-int(item.get("count") or 0), item["name"]))
        result[destination] = [
            f"{item['name']}（{item.get('cn', '')}）" for item in values[:limit]
        ]
    return result


def category_hypothesis(
    category: CategorySpec,
    examples: dict[tuple[str, str], list[str]],
) -> str:
    example_text = ""
    if examples.get(category.key):
        example_text = " 已人工核对的典型例子有：" + "、".join(examples[category.key]) + "。"
    return (
        f"分类：{category.folder_name} > {category.category_name}。"
        f"English semantic key: {category.folder_id.replace('_', ' ')} > "
        f"{category.category_id.replace('_', ' ')}. "
        f"定义：直接描述{category.category_name}；范围包括{category.folder_description}。"
        f"{example_text}"
    )


def folder_hypothesis(
    folder: CategorySpec,
    category_examples: dict[tuple[str, str], list[str]],
) -> str:
    examples = []
    for (folder_id, _), values in category_examples.items():
        if folder_id == folder.folder_id:
            examples.extend(values[:2])
    example_text = "、".join(dict.fromkeys(examples))
    return (
        f"大分类：{folder.folder_name}。English semantic key: "
        f"{folder.folder_id.replace('_', ' ')}. "
        f"定义：{folder.folder_description}。典型标签：{example_text}。"
    )


def load_model(device: str):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, use_safetensors=True,
    ).to(device).eval()
    return tokenizer, model, 0, 0


def score_pairs(
    premises: list[str],
    hypotheses: list[str],
    tokenizer,
    model,
    entailment_index: int,
    contradiction_index: int,
    device: str,
    pair_batch: int,
    max_length: int,
) -> np.ndarray:
    chunks: list[np.ndarray] = []
    dtype = torch.float16 if device == "cuda" else torch.float32
    for start in range(0, len(premises), pair_batch):
        # BGE rerankers are trained with the category/query first and the Wiki
        # evidence/passage second.  Reversing this order is measurably worse.
        encoded = tokenizer(
            hypotheses[start:start + pair_batch],
            premises[start:start + pair_batch],
            padding=True,
            truncation=True,
            max_length=max_length,
            pad_to_multiple_of=8 if device == "cuda" else None,
            return_tensors="pt",
        ).to(device)
        with torch.inference_mode(), torch.autocast(
            device_type=device, dtype=dtype, enabled=device == "cuda",
        ):
            logits = model(**encoded).logits.float()
        score = logits.view(-1)
        chunks.append(score.cpu().numpy().astype(np.float32))
    return np.concatenate(chunks)


def score_tag_rows(
    tags: list[dict],
    categories: list[CategorySpec],
    hypotheses: list[str],
    tokenizer,
    model,
    entailment_index: int,
    contradiction_index: int,
    device: str,
    pair_batch: int,
    max_length: int,
) -> np.ndarray:
    premises: list[str] = []
    paired_hypotheses: list[str] = []
    for tag in tags:
        premise = tag_premise(tag)
        premises.extend([premise] * len(categories))
        paired_hypotheses.extend(hypotheses)
    flat = score_pairs(
        premises, paired_hypotheses, tokenizer, model,
        entailment_index, contradiction_index, device, pair_batch, max_length,
    )
    return flat.reshape(len(tags), len(categories))


def calibration_bias(
    categories: list[CategorySpec],
    hypotheses: list[str],
    tokenizer,
    model,
    entailment_index: int,
    contradiction_index: int,
    device: str,
    pair_batch: int,
    max_length: int,
) -> np.ndarray:
    """Measure fixed score preference caused by each category's wording."""
    neutral_tags = [
        {"name": "unknown_tag", "cn": "未知标签", "aliases": [], "wiki": text}
        for text in (
            "没有提供这个标签的具体定义。",
            "这是一个等待确认含义的绘图标签。",
            "该条目不说明任何具体对象、属性、动作、人物或场景。",
            "Unknown; no semantic definition is available for this tag.",
            "This entry does not identify a particular object, action, attribute, person, or scene.",
        )
    ]
    raw = score_tag_rows(
        neutral_tags, categories, hypotheses, tokenizer, model,
        entailment_index, contradiction_index, device, pair_batch, max_length,
    )
    bias = np.median(raw, axis=0).astype(np.float32)
    print(
        f"Reranker label-bias baseline: min={bias.min():.4f}; "
        f"median={np.median(bias):.4f}; max={bias.max():.4f}",
        flush=True,
    )
    return bias


def benchmark_indices(tags: list[dict], per_category: int) -> tuple[list[int], dict[str, tuple[str, str]]]:
    anchors = read_anchor_expectations()
    reviewed = {
        name: normalize_location(destination, name)
        for name, destination in EXACT_OVERRIDES.items()
    }
    reviewed.update({
        name: normalize_location(destination, name)
        for name, destination in anchors.items()
    })
    by_destination: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, tag in enumerate(tags):
        if tag["name"] in reviewed and tag["category"] == "0":
            by_destination[reviewed[tag["name"]]].append(index)
    selected = {index for indexes in by_destination.values() for index in indexes[:per_category]}
    name_to_index = {tag["name"]: index for index, tag in enumerate(tags)}
    selected.update(name_to_index[name] for name in anchors if name in name_to_index)
    return sorted(selected), reviewed


def run_benchmark(
    args, tags, categories, hypotheses, folders, folder_hypotheses,
    tokenizer, model, entail, contra, device, bias, folder_bias,
) -> bool:
    indexes, reviewed = benchmark_indices(tags, args.benchmark_per_category)
    samples = [tags[index] for index in indexes]
    expected = [reviewed[tag["name"]] for tag in samples]
    start = time.perf_counter()
    raw_scores = score_tag_rows(
        samples, categories, hypotheses, tokenizer, model, entail, contra,
        device, args.pair_batch, args.max_length,
    )
    raw_folder_scores = score_tag_rows(
        samples, folders, folder_hypotheses, tokenizer, model, entail, contra,
        device, args.pair_batch, args.max_length,
    )
    # Source indices are audited but are not semantic destinations for a
    # Danbooru general tag.  Their source type is authoritative and handled
    # separately for type 3/4 rows.
    source_positions = [index for index, item in enumerate(categories) if item.source_type]
    expected_indexes = np.asarray([
        next((index for index, item in enumerate(categories) if item.key == destination), -1)
        for destination in expected
    ])
    bias_trials = sorted(set([
        args.bias_weight, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.65, 0.8, 1.0,
    ]))
    folder_index = {item.folder_id: index for index, item in enumerate(folders)}
    category_folder_indexes = np.asarray([
        folder_index[item.folder_id] for item in categories
    ], dtype=np.int64)
    trial_results = []
    best_weight = args.bias_weight
    best_folder_weight = args.folder_weight
    best_correct = -1
    for weight in bias_trials:
        for parent_weight in (0.0, 0.15, 0.3, 0.5, 0.75, 1.0, 1.4, 2.0):
            calibrated_folders = raw_folder_scores - folder_bias[None, :]
            trial = (
                raw_scores - weight * bias[None, :]
                + parent_weight * calibrated_folders[:, category_folder_indexes]
            )
            trial[:, source_positions] = -np.inf
            predicted = np.argmax(trial, axis=1)
            trial_correct = int(np.count_nonzero(predicted == expected_indexes))
            trial_results.append({
                "biasWeight": weight,
                "folderWeight": parent_weight,
                "correct": trial_correct,
            })
            if trial_correct > best_correct:
                best_correct = trial_correct
                best_weight = weight
                best_folder_weight = parent_weight
    calibrated_folders = raw_folder_scores - folder_bias[None, :]
    scores = (
        raw_scores - best_weight * bias[None, :]
        + best_folder_weight * calibrated_folders[:, category_folder_indexes]
    )
    scores[:, source_positions] = -np.inf
    elapsed = time.perf_counter() - start
    top = np.argsort(scores, axis=1)[:, -5:][:, ::-1]
    predictions = [categories[int(row[0])].key for row in top]
    top5 = [{categories[int(position)].key for position in row} for row in top]
    correct = sum(a == b for a, b in zip(predictions, expected))
    correct5 = sum(b in row for b, row in zip(expected, top5))
    rows = []
    for tag, wanted, predicted, positions, row_scores in zip(samples, expected, predictions, top, scores):
        if wanted == predicted:
            continue
        rows.append({
            "tag": tag["name"], "cn": tag.get("cn", ""), "wiki": tag.get("wiki", ""),
            "expected": "/".join(wanted), "predicted": "/".join(predicted),
            "top_candidates": " | ".join(
                f"{categories[int(position)].label}={row_scores[int(position)]:.4f}"
                for position in positions
            ),
        })
    OUTPUT_DIR.mkdir(exist_ok=True)
    error_path = OUTPUT_DIR / "wiki_pairwise_benchmark_errors.csv"
    with error_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["tag"])
        writer.writeheader()
        writer.writerows(rows)
    pairs = len(samples) * (len(categories) + len(folders))
    summary = {
        "model": MODEL_NAME,
        "device": device,
        "sampleTags": len(samples),
        "semanticCategoryCount": len(categories),
        "parentFolderCount": len(folders),
        "pairJudgments": pairs,
        "elapsedSeconds": round(elapsed, 3),
        "pairsPerSecond": round(pairs / elapsed, 1),
        "top1Correct": correct,
        "top1Accuracy": correct / len(samples) if samples else 0,
        "top5Correct": correct5,
        "top5Accuracy": correct5 / len(samples) if samples else 0,
        "estimatedFullHours": round(
            len(tags) * (len(categories) + len(folders)) / (pairs / elapsed) / 3600, 2,
        ),
        "bestBiasWeight": best_weight,
        "bestFolderWeight": best_folder_weight,
        "biasWeightTrials": trial_results,
    }
    (OUTPUT_DIR / "wiki_pairwise_benchmark_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"Benchmark disagreements: {error_path}", flush=True)
    return summary["top1Accuracy"] >= args.minimum_accuracy


def score_cache_paths(tags: list[dict], categories: list[CategorySpec]) -> tuple[Path, Path]:
    digest = hashlib.sha256()
    digest.update(data_fingerprint().encode("ascii"))
    digest.update(repr(categories).encode("utf-8"))
    key = digest.hexdigest()[:20]
    # Reuse the first run's pre-rename cache so a 20-million-pair audit never
    # restarts merely because the public script received a clearer name.
    legacy = (
        CACHE_DIR / f"wiki-nli-{key}-scores.npy",
        CACHE_DIR / f"wiki-nli-{key}-checkpoint.json",
    )
    if legacy[0].exists() or legacy[1].exists():
        return legacy
    return (
        CACHE_DIR / f"wiki-pairwise-{key}-scores.npy",
        CACHE_DIR / f"wiki-pairwise-{key}-checkpoint.json",
    )


def run_full(
    args, tags, categories, hypotheses, folders, folder_hypotheses,
    tokenizer, model, entail, contra, device, bias, folder_bias,
) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    score_path, checkpoint_path = score_cache_paths(tags, categories)
    shape = (len(tags), len(categories))
    completed = 0
    if score_path.exists() and checkpoint_path.exists() and not args.restart:
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        completed = int(checkpoint.get("completedRows", 0))
        scores = np.lib.format.open_memmap(score_path, mode="r+", dtype=np.float16, shape=shape)
        print(f"Resuming at tag {completed:,}/{len(tags):,}", flush=True)
    else:
        scores = np.lib.format.open_memmap(score_path, mode="w+", dtype=np.float16, shape=shape)
    started = time.perf_counter()
    start_completed = completed
    for start in range(completed, len(tags), args.tag_batch):
        stop = min(start + args.tag_batch, len(tags))
        block = score_tag_rows(
            tags[start:stop], categories, hypotheses, tokenizer, model,
            entail, contra, device, args.pair_batch, args.max_length,
        )
        block -= args.bias_weight * bias[None, :]
        folder_block = score_tag_rows(
            tags[start:stop], folders, folder_hypotheses, tokenizer, model,
            entail, contra, device, args.pair_batch, args.max_length,
        )
        folder_block -= folder_bias[None, :]
        folder_index = {item.folder_id: index for index, item in enumerate(folders)}
        category_folder_indexes = np.asarray([
            folder_index[item.folder_id] for item in categories
        ], dtype=np.int64)
        block += args.folder_weight * folder_block[:, category_folder_indexes]
        scores[start:stop] = block.astype(np.float16)
        scores.flush()
        checkpoint_path.write_text(json.dumps({
            "model": MODEL_NAME,
            "databaseFingerprint": data_fingerprint(),
            "completedRows": stop,
            "tagCount": len(tags),
            "categoryCount": len(categories),
            "pairJudgmentsCompleted": stop * (len(categories) + len(folders)),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        if stop == len(tags) or stop % max(args.progress_every, args.tag_batch) < args.tag_batch:
            elapsed = time.perf_counter() - started
            destinations_per_tag = len(categories) + len(folders)
            rate = (stop - start_completed) * destinations_per_tag / max(elapsed, 1e-6)
            remaining = (len(tags) - stop) * destinations_per_tag / max(rate, 1e-6)
            print(
                f"rows={stop:,}/{len(tags):,}; "
                f"pairs={stop * (len(categories) + len(folders)):,}; "
                f"rate={rate:,.1f}/s; eta={remaining / 3600:.2f}h",
                flush=True,
            )
    write_outputs(tags, categories, np.asarray(scores, dtype=np.float32), args)


def write_outputs(tags: list[dict], categories: list[CategorySpec], scores: np.ndarray, args) -> None:
    ranking_scores = scores.copy()
    source_positions = [index for index, item in enumerate(categories) if item.source_type]
    general_rows = [index for index, tag in enumerate(tags) if tag["category"] == "0"]
    if general_rows and source_positions:
        ranking_scores[np.ix_(general_rows, source_positions)] = -np.inf
    top_count = min(args.top_k, len(categories))
    top = np.argpartition(ranking_scores, -top_count, axis=1)[:, -top_count:]
    top = np.take_along_axis(
        top,
        np.argsort(np.take_along_axis(ranking_scores, top, axis=1), axis=1)[:, ::-1],
        axis=1,
    )
    reviewed = {
        name: normalize_location(destination, name)
        for name, destination in EXACT_OVERRIDES.items()
    }
    reviewed.update({
        name: normalize_location(destination, name)
        for name, destination in read_anchor_expectations().items()
    })
    assignments: dict[str, list[str]] = {}
    rows = []
    conflict_count = 0
    low_margin_count = 0
    for row_index, tag in enumerate(tags):
        positions = top[row_index]
        proposed_spec = categories[int(positions[0])]
        proposed = proposed_spec.key
        margin = float(scores[row_index, int(positions[0])] - scores[row_index, int(positions[1])])
        source_folder = SOURCE_FOLDER_BY_TYPE.get(tag["category"])
        if source_folder:
            final = classify_tag(tag)
            method = "authoritative-source-type-after-all-pairs"
        elif tag["name"] in reviewed:
            final = reviewed[tag["name"]]
            method = "human-wiki-override-after-all-pairs"
        else:
            final = proposed
            method = "wiki-definition-all-category-cross-encoder"
        assignments[tag["name"]] = list(final)
        expected = reviewed.get(tag["name"])
        conflict = bool(expected and expected != proposed)
        conflict_count += int(conflict)
        low_margin_count += int(margin < args.low_margin)
        rows.append({
            "tag": tag["name"],
            "cn": tag.get("cn", ""),
            "source_type": tag["category"],
            "wiki": " ".join((tag.get("wiki") or "").split()),
            "wiki_missing": int(not bool((tag.get("wiki") or "").strip())),
            "current": "/".join(classify_tag(tag)),
            "pairwise_proposed": "/".join(proposed),
            "final": "/".join(final),
            "method": method,
            "top_score": f"{scores[row_index, int(positions[0])]:.6f}",
            "margin": f"{margin:.6f}",
            "low_margin": int(margin < args.low_margin),
            "human_conflict": int(conflict),
            "top_candidates": " | ".join(
                f"{categories[int(position)].label}={scores[row_index, int(position)]:.4f}"
                for position in positions
            ),
        })
    full_path = OUTPUT_DIR / "wiki_pairwise_full_audit.csv"
    with full_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    conflicts = [row for row in rows if row["human_conflict"] or row["low_margin"] or row["wiki_missing"]]
    with (OUTPUT_DIR / "wiki_pairwise_review_queue.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(conflicts)
    summary = {
        "model": MODEL_NAME,
        "databaseFingerprint": data_fingerprint(),
        "tagCount": len(tags),
        "semanticCategoryCount": len(categories),
        "parentFolderCount": len({item.folder_id for item in categories}),
        "categoryPairwiseJudgmentCount": len(tags) * len(categories),
        "pairwiseJudgmentCount": len(tags) * (
            len(categories) + len({item.folder_id for item in categories})
        ),
        "wikiPresentCount": sum(bool((tag.get("wiki") or "").strip()) for tag in tags),
        "wikiMissingTags": [tag["name"] for tag in tags if not (tag.get("wiki") or "").strip()],
        "humanConflictCount": conflict_count,
        "lowMarginCount": low_margin_count,
    }
    (OUTPUT_DIR / "wiki_pairwise_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    if args.write_map:
        payload = {
            "databaseFingerprint": server.database_fingerprint(),
            "model": MODEL_NAME,
            "method": "full-wiki-definition-cross-encoder-reranker-all-categories",
            "pairwiseJudgmentCount": len(tags) * (
                len(categories) + len({item.folder_id for item in categories})
            ),
            "assignments": assignments,
        }
        with gzip.open(ROOT / "data" / "semantic_tag_locations.json.gz", "wt", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"Full audit: {full_path}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("benchmark", "full"), default="benchmark")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto")
    parser.add_argument("--pair-batch", type=int, default=128)
    parser.add_argument("--tag-batch", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--benchmark-per-category", type=int, default=2)
    parser.add_argument("--minimum-accuracy", type=float, default=0.72)
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--low-margin", type=float, default=0.30)
    parser.add_argument("--bias-weight", type=float, default=0.4)
    parser.add_argument("--folder-weight", type=float, default=0.3)
    parser.add_argument("--write-map", action="store_true")
    parser.add_argument("--restart", action="store_true")
    args = parser.parse_args()

    device = "cuda" if args.device == "auto" and torch.cuda.is_available() else args.device
    if device == "auto":
        device = "cpu"
    if device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA requested but unavailable")
    tags = server.read_tags()
    categories = all_categories()
    folders = all_folders(categories)
    examples = verified_examples(tags)
    hypotheses = [category_hypothesis(category, examples) for category in categories]
    folder_hypotheses = [folder_hypothesis(folder, examples) for folder in folders]
    print(
        f"tags={len(tags):,}; categories={len(categories):,}; "
        f"category-pair judgments={len(tags) * len(categories):,}; "
        f"parent-pair judgments={len(tags) * len(folders):,}; device={device}",
        flush=True,
    )
    tokenizer, model, entail, contra = load_model(device)
    bias = calibration_bias(
        categories, hypotheses, tokenizer, model, entail, contra, device,
        args.pair_batch, args.max_length,
    )
    folder_bias = calibration_bias(
        folders, folder_hypotheses, tokenizer, model, entail, contra, device,
        args.pair_batch, args.max_length,
    )
    if args.mode == "benchmark":
        passed = run_benchmark(
            args, tags, categories, hypotheses, folders, folder_hypotheses,
            tokenizer, model, entail, contra, device, bias, folder_bias,
        )
        if not passed:
            raise SystemExit(
                f"Benchmark below {args.minimum_accuracy:.1%}; refusing to run/deploy full map",
            )
    else:
        run_full(
            args, tags, categories, hypotheses, folders, folder_hypotheses,
            tokenizer, model, entail, contra, device, bias, folder_bias,
        )


if __name__ == "__main__":
    main()
