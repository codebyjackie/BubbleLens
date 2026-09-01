"""Small development report for auditing the deterministic tag taxonomy."""

from __future__ import annotations

import argparse
from collections import Counter

import server


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="other")
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--ngrams", type=int, choices=(1, 2, 3), default=0)
    parser.add_argument("--find", nargs="*", default=[])
    args = parser.parse_args()

    catalog = server.build_catalog()
    if args.find:
        wanted = set(args.find)
        for folder in catalog["folders"]:
            for category in folder["categories"]:
                for tag in category["tags"]:
                    if tag["name"] in wanted:
                        print(f"{tag['name']}\t{folder['id']}/{category['id']}\t{folder['name']} / {category['name']}")
        return
    folder = next(item for item in catalog["folders"] if item["id"] == args.folder)
    tags = sorted(
        (tag for category in folder["categories"] for tag in category["tags"]),
        key=lambda item: (-item["count"], item["name"]),
    )
    print(
        f"rows={catalog['sourceRowCount']} unique={catalog['tagCount']} "
        f"fallback={catalog['fallbackCount']} folder={folder['name']} tags={len(tags)}"
    )
    if args.ngrams:
        grams = Counter()
        for tag in tags:
            text = tag.get("cn", "")
            for index in range(len(text) - args.ngrams + 1):
                gram = text[index : index + args.ngrams]
                if gram.strip() and not any(char in gram for char in "（）() /_-，,·"):
                    grams[gram] += 1
        for gram, count in grams.most_common(args.limit):
            print(f"{count}\t{gram}")
        return
    for tag in tags[: args.limit]:
        wiki = tag.get("wiki", "").replace("\n", " ")[:90]
        print(f"{tag['count']}\t{tag['name']}\t{tag.get('cn', '')[:40]}\t{wiki}")


if __name__ == "__main__":
    main()
