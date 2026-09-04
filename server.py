from __future__ import annotations

import csv
import gzip
import json
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from taxonomy import TAXONOMY, classify_tag


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tags_enhanced.csv"
LOCATION_FILE = ROOT / "data" / "semantic_tag_locations.json.gz"
HOST = "127.0.0.1"
PORT = int(os.environ.get("BUBBLELENS_PORT", os.environ.get("PROMPT_GENERATOR_PORT", "7873")))
CATALOG_VERSION = 20

# Corrections for source aliases whose literal Chinese label conflicts with the
# bundled wiki definition.  Keeping them here preserves the source CSV while
# ensuring search results, cards and tooltips all show the corrected meaning.
TAG_ALIAS_OVERRIDES = {
    "deep_skin": ["抓握深陷", "皮肉深陷", "深度压陷"],
    "batter": ["面糊", "面浆", "烘焙面糊"],
    "legskin": ["连腿泳裤", "长腿竞速泳装", "男式竞速泳装"],
    "skin_fang": ["单侧口缘虎牙", "肤色虎牙", "口缘尖牙"],
    "skin_fangs": ["双侧口缘虎牙", "肤色双虎牙", "口缘尖牙"],
    "load_bearing_equipment": ["携行装备", "战术携行具", "携行具"],
    "sett": ["铺路石", "石砌路面", "方形铺路石"],
    "yuri_(object)": ["百合题材物品", "百合作品物件", "百合题材漫画"],
    "pokemon_(anime)": ["宝可梦（动画）", "精灵宝可梦（动画）", "宝可梦动画系列"],
}


def read_tags() -> list[dict]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"标签数据库不存在：{DATA_FILE}")
    by_name = {}
    with DATA_FILE.open("r", encoding="gb18030", newline="") as handle:
        for row in csv.DictReader(handle):
            name = (row.get("name") or "").strip()
            if not name:
                continue
            aliases = [item.strip() for item in (row.get("cn_name") or "").split(",") if item.strip()]
            candidate = {
                "id": name,
                "name": name,
                "cn": aliases[0] if aliases else name.replace("_", " "),
                "aliases": aliases[:4],
                "wiki": (row.get("wiki") or "").strip(),
                "count": int(row.get("post_count") or 0),
                "nsfw": row.get("nsfw") == "1",
                "category": row.get("category") or "0",
            }
            existing = by_name.get(name)
            if existing is None:
                by_name[name] = candidate
                continue
            combined_aliases = list(dict.fromkeys(existing["aliases"] + candidate["aliases"]))
            existing["aliases"] = combined_aliases[:8]
            if candidate["aliases"] and (not existing["cn"] or len(candidate["cn"]) > len(existing["cn"])):
                existing["cn"] = candidate["cn"]
            if len(candidate["wiki"]) > len(existing["wiki"]):
                existing["wiki"] = candidate["wiki"]
            existing["count"] = max(existing["count"], candidate["count"])
            existing["nsfw"] = existing["nsfw"] or candidate["nsfw"]
    for name, aliases in TAG_ALIAS_OVERRIDES.items():
        tag = by_name.get(name)
        if tag:
            tag["cn"] = aliases[0]
            tag["aliases"] = aliases
    return list(by_name.values())


def read_tag_locations(tags: list[dict]) -> dict[str, tuple[str, str]]:
    if not LOCATION_FILE.exists():
        raise FileNotFoundError(f"完整分类位置表不存在：{LOCATION_FILE}")
    with gzip.open(LOCATION_FILE, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    assignments = payload.get("assignments") or {}
    tag_names = {tag["name"] for tag in tags}
    if set(assignments) != tag_names:
        missing = len(tag_names - set(assignments))
        extra = len(set(assignments) - tag_names)
        raise RuntimeError(f"完整分类位置表与数据库不匹配：缺少 {missing}，多出 {extra}")
    return {name: tuple(location) for name, location in assignments.items()}


def build_catalog() -> dict:
    tags = read_tags()
    tag_locations = read_tag_locations(tags)
    folders = []
    buckets = {}
    for folder_spec in TAXONOMY:
        current = {key: value for key, value in folder_spec.items() if key != "categories"}
        current["categories"] = []
        for category_spec in folder_spec["categories"]:
            item = {"id": category_spec["id"], "name": category_spec["name"], "tags": []}
            current["categories"].append(item)
            buckets[(current["id"], item["id"])] = item["tags"]
        folders.append(current)

    for tag in tags:
        # Reviewed rules must never be overwritten by a low-confidence vector
        # winner. The complete semantic table is only the last resort for tags
        # that the deterministic classifier still cannot place.
        stable_location = classify_tag(tag)
        location = stable_location if stable_location[0] != "other" else tag_locations[tag["name"]]
        if location not in buckets:
            raise RuntimeError(f"分类器返回了不存在的位置：{tag['name']} -> {location}")
        buckets[location].append(tag)

    for current in folders:
        current["tagCount"] = 0
        nonempty = []
        for item in current["categories"]:
            item["tags"].sort(key=lambda tag: (-tag["count"], tag["name"]))
            item["tagCount"] = len(item["tags"])
            current["tagCount"] += item["tagCount"]
            if item["tags"]:
                nonempty.append(item)
        current["categories"] = nonempty

    fallback_count = sum(folder["tagCount"] for folder in folders if folder["id"] == "other")
    assigned_count = sum(folder["tagCount"] for folder in folders)
    if assigned_count != len(tags):
        raise RuntimeError(f"标签覆盖不完整：{assigned_count}/{len(tags)}")
    return {
        "folders": folders,
        "tagCount": assigned_count,
        "sourceCount": len(tags),
        "sourceRowCount": 49844,
        "fallbackCount": fallback_count,
        "version": CATALOG_VERSION,
    }


_catalog_lock = threading.Lock()
_catalog_cache = None


def get_catalog() -> dict:
    global _catalog_cache
    with _catalog_lock:
        if _catalog_cache is None:
            _catalog_cache = build_catalog()
    return _catalog_cache


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("[BubbleLens] " + fmt % args)

    def send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        use_gzip = len(body) > 1024 and "gzip" in self.headers.get("Accept-Encoding", "").lower()
        if use_gzip:
            body = gzip.compress(body, compresslevel=5)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        if use_gzip:
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/catalog":
            try:
                self.send_json(200, get_catalog())
            except Exception as exc:
                self.send_json(500, {"error": str(exc)})
            return
        if path == "/api/health":
            self.send_json(200, {"ok": True, "database": DATA_FILE.exists(), "app": "bubblelens", "version": CATALOG_VERSION})
            return
        if path == "/api/shutdown":
            self.send_json(200, {"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/shutdown":
            self.send_json(200, {"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        self.send_json(404, {"error": "not found"})


def main():
    print(f"BubbleLens：http://{HOST}:{PORT}")
    print(f"标签数据库：{DATA_FILE}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    no_browser = os.environ.get("BUBBLELENS_NO_BROWSER", os.environ.get("PROMPT_GENERATOR_NO_BROWSER"))
    if no_browser != "1" and "--no-browser" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://{HOST}:{PORT}")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
