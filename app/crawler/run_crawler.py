import json
from pathlib import Path

from app.crawler.fetch_posts import fetch_posts
from app.crawler.product_detector import is_product_post
from app.crawler.extractor import extract_product

from app.session.session_manager import SessionManager
from app.session.rate_limiter import RateLimiter
from app.session.backoff import Backoff


INPUT_FILE = Path("data/validated_channels.json")
OUTPUT_FILE_FALLBACK = Path("data/products_crawled.json")


def _redis_available():
    """بررسی در دسترس بودن Redis"""
    try:
        from app.queue.redis_conn import redis_conn
        redis_conn.ping()
        return True
    except Exception:
        return False


def run():
    if not INPUT_FILE.exists():
        print("validated_channels.json not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    print(f"[+] crawling {len(channels)} channels")

    use_redis = _redis_available()
    if use_redis:
        from app.queue.product_queue import product_queue
        from app.worker.product_worker import process_product
        print("[+] Redis در دسترس است. محصولات به صف Redis ارسال می‌شوند.")
    else:
        print("[!] Redis در دسترس نیست. محصولات در فایل ذخیره می‌شوند.")
        products_fallback = []

    total_jobs = 0
    sessions = ["acc1", "acc2", "acc3"]
    session_manager = SessionManager(sessions)
    rate_limiter = RateLimiter(rate_per_sec=2)
    backoff = Backoff()

    for ch in channels:
        print(f"[+] channel: {ch['channel_id']}")
        session = session_manager.get_session()
        rate_limiter.wait()

        try:
            posts = fetch_posts(ch)
            backoff.success()
        except Exception as e:
            print("request failed:", e)
            backoff.fail()
            continue

        for post in posts:
            if is_product_post(post):
                product = extract_product(post, ch["channel_id"])
                if use_redis:
                    product_queue.enqueue(process_product, product)
                else:
                    products_fallback.append(product)
                total_jobs += 1

    if use_redis:
        print(f"[✓] {total_jobs} jobs به صف Redis ارسال شد.")
    else:
        OUTPUT_FILE_FALLBACK.parent.mkdir(exist_ok=True)
        with open(OUTPUT_FILE_FALLBACK, "w", encoding="utf-8") as f:
            json.dump(products_fallback, f, ensure_ascii=False, indent=2)
        print(f"[✓] {total_jobs} محصول در {OUTPUT_FILE_FALLBACK} ذخیره شد.")


if __name__ == "__main__":
    run()
