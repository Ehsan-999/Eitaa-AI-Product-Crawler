import json
from pathlib import Path

from app.validation.fetch_channel_preview import fetch_preview
from app.validation.classifier import is_shop_channel


INPUT_FILE = Path("data/channels.json")
OUTPUT_FILE = Path("data/validated_channels.json")


def run():
    if not INPUT_FILE.exists():
        print("channels.json not found. Run discovery first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    print(f"[+] loaded {len(channels)} channels")

    validated = []

    for ch in channels:
        preview = fetch_preview(ch)
        result = is_shop_channel(preview)

        if result["is_shop"]:
            validated.append(ch)

        print(
            f"{ch['channel_id']} -> shop={result['is_shop']} score={result['score']}"
        )

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(validated, f, ensure_ascii=False, indent=2)

    print(f"[✓] {len(validated)} shop channels saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
