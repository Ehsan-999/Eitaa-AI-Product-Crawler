import os
import json
from pathlib import Path

from app.discovery.keywords import generate_keywords
from app.discovery.search import search_channels


OUTPUT_FILE = Path("data/channels.json")


def run():
    all_channels = []
    channel_ids = os.getenv("EITAA_CHANNEL_IDS", "").strip()
    if channel_ids:
        print("[+] Using EITAA_CHANNEL_IDS (real Eitaa channels)")
        channels = search_channels("")
        all_channels.extend(channels)
    else:
        keywords = generate_keywords()
        print(f"[+] {len(keywords)} keywords generated")
        for kw in keywords:
            print(f"[+] searching for: {kw}")
            channels = search_channels(kw)
            all_channels.extend(channels)

    unique = {c["channel_id"]: c for c in all_channels}.values()

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(unique), f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(unique)} channels saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
