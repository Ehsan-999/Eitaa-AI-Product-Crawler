"""
خالی کردن صف محصولات (Redis Queue)
قبل از crawl جدید اجرا کن تا فقط داده‌های جدید پردازش شوند.
"""
import sys

def main():
    try:
        from app.queue.product_queue import product_queue
        from app.queue.redis_conn import redis_conn
        redis_conn.ping()
    except Exception as e:
        print(f"[!] Redis در دسترس نیست: {e}")
        print("    اگر Redis نمی‌خواهی، ورکر لازم نیست؛ خروجی در data/products_crawled.json است.")
        return 1

    count_before = len(product_queue)
    product_queue.empty()
    print(f"[✓] صف «products» خالی شد. ({count_before} job حذف شد)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
