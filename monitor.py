import asyncio
import json
import os
import time
from datetime import datetime, timezone

from TikTokApi import TikTokApi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def score(video: dict, weights: dict) -> float:
    stats = video.get("stats", {})
    views = stats.get("playCount", 0) or 0
    likes = stats.get("diggCount", 0) or 0
    shares = stats.get("shareCount", 0) or 0
    return (
        views * weights["views"]
        + likes * weights["likes"]
        + shares * weights["shares"]
    )


def format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def time_ago(ts: int) -> str:
    diff = int(time.time()) - ts
    hours = diff // 3600
    minutes = (diff % 3600) // 60
    if hours > 0:
        return f"vor {hours} Std."
    return f"vor {minutes} Min."


def is_relevant(video: dict, relevance: dict) -> bool:
    desc = (video.get("desc") or "").lower()
    account = (video.get("author", {}).get("uniqueId") or "").lower()
    hashtags = " ".join(
        c.get("title", "") for c in video.get("challenges", [])
    ).lower()
    text = f"{desc} {hashtags}"

    all_keywords = (
        relevance["keywords_steiermark"]
        + relevance["keywords_kaernten"]
        + relevance["keywords_austria_general"]
    )
    if any(kw in text for kw in all_keywords):
        return True
    if any(acc in account for acc in relevance["trusted_accounts"]):
        return True
    return False


def detect_region(video: dict, relevance: dict) -> str:
    desc = (video.get("desc") or "").lower()
    hashtags = " ".join(
        c.get("title", "") for c in video.get("challenges", [])
    ).lower()
    text = f"{desc} {hashtags}"

    in_stmk = any(kw in text for kw in relevance["keywords_steiermark"])
    in_ktn = any(kw in text for kw in relevance["keywords_kaernten"])

    if in_stmk and in_ktn:
        return "Kärnten & Steiermark"
    if in_stmk:
        return "Steiermark"
    if in_ktn:
        return "Kärnten"
    return "Österreich"


def build_output(cfg: dict, videos: list) -> dict:
    entries = []
    for i, v in enumerate(videos, 1):
        stats = v.get("stats", {})
        author = v.get("author", {})
        hashtags = [
            f"#{c.get('title', '')}"
            for c in v.get("challenges", [])
            if c.get("title")
        ]
        video_id = v.get("id", "")
        author_id = author.get("uniqueId", "")
        url = f"https://www.tiktok.com/@{author_id}/video/{video_id}"

        entries.append({
            "rank": i,
            "title": v.get("desc", "")[:120],
            "url": url,
            "thumbnail": v.get("video", {}).get("cover", ""),
            "account": author_id,
            "views": format_number(stats.get("playCount", 0) or 0),
            "likes": format_number(stats.get("diggCount", 0) or 0),
            "shares": format_number(stats.get("shareCount", 0) or 0),
            "comments": format_number(stats.get("commentCount", 0) or 0),
            "uploaded": time_ago(v.get("createTime", 0)),
            "region": detect_region(v, cfg["relevance"]),
            "hashtags": hashtags[:8],
            "synopsis": "",
            "notes": ""
        })

    return {
        "meta": {
            "stand": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "zeitraum": f"letzte {cfg['hours_back']} Stunden",
            "regionen": ["Kärnten", "Steiermark"],
            "erstellt_von": "monitor.py"
        },
        "videos": entries
    }


async def main():
    cfg = load_config()
    cutoff = int(time.time()) - cfg["hours_back"] * 3600
    weights = cfg["score_weights"]
    seen = {}

    print(f"Starte Monitoring — {len(cfg['hashtags'])} Hashtags, letzte {cfg['hours_back']}h\n")

    relevance = cfg["relevance"]

    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[cfg["ms_token"]],
            num_sessions=1,
            sleep_after=3,
            headless=True
        )

        for tag_name in cfg["hashtags"]:
            print(f"  #{tag_name} ...")
            try:
                tag = api.hashtag(name=tag_name)
                async for video in tag.videos(count=cfg["max_videos_per_hashtag"]):
                    raw = video.as_dict
                    vid_id = raw.get("id")
                    if not vid_id or raw.get("createTime", 0) < cutoff:
                        continue
                    if not is_relevant(raw, relevance):
                        continue
                    if vid_id not in seen or score(raw, weights) > score(seen[vid_id], weights):
                        seen[vid_id] = raw
            except Exception as e:
                print(f"    Fehler bei #{tag_name}: {e}")
            await asyncio.sleep(2)

    print(f"\n{len(seen)} relevante Videos gefunden.")
    ranked = sorted(seen.values(), key=lambda v: score(v, weights), reverse=True)
    top = ranked[:cfg["top_n"]]

    output = build_output(cfg, top)

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_path = os.path.join(BASE_DIR, cfg["output_dir"], f"{date_str}_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nFertig — {len(top)} Videos gespeichert: {out_path}")
    print("Dashboard öffnen und JSON laden: dashboards/dashboard_tiktok_trending.html")


if __name__ == "__main__":
    asyncio.run(main())
