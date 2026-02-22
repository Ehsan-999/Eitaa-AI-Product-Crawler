"""
Eitaa Product Crawler - Main Pipeline
اجرای کامل Pipeline از Discovery تا Crawling
"""

import argparse
import sys

from app.discovery.run_discovery import run as run_discovery
from app.validation.run_validation import run as run_validation
from app.crawler.run_crawler import run as run_crawler


def safe_run(name, func):
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    try:
        func()
    except Exception as e:
        print(f"[ERROR] {name} failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Eitaa Product Crawler Pipeline"
    )
    parser.add_argument(
        "phase",
        choices=["discovery", "validation", "crawl", "all"],
        help="فاز اجرا: discovery, validation, crawl, یا all",
    )

    args = parser.parse_args()

    if args.phase in ["discovery", "all"]:
        safe_run(
            "Phase 1: Discovery - تولید کلمات کلیدی و جستجو",
            run_discovery,
        )

    if args.phase in ["validation", "all"]:
        safe_run(
            "Phase 2: Validation - اعتبارسنجی کانال‌ها",
            run_validation,
        )

    if args.phase in ["crawl", "all"]:
        safe_run(
            "Phase 3: Crawling - خزش و استخراج محصولات",
            run_crawler,
        )

    print("\n" + "=" * 50)
    print("Pipeline completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()