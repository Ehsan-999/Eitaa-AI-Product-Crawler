import os
import random
from app.eitaa.sync_wrapper import get_channel_posts as eitaa_get_posts

PRODUCT_WORDS = [
    "موجود",
    "ارسال رایگان",
    "برای سفارش دایرکت",
    "خرید فوری",
]

NORMAL_WORDS = [
    "امروز تعطیل است",
    "پست جدید",
    "تبلیغات",
    "اطلاعیه",
    "خبر",
]

# محدوده قیمت برای mock (هزار تومان تا چند میلیون)
MOCK_PRICE_RANGES = [
    (50, 500),      # 50 تا 500 هزار
    (500, 2000),    # 500 هزار تا 2 میلیون
    (2000, 10000),  # 2 تا 10 میلیون
]


def fake_post(is_product: bool, idx: int):
    words = PRODUCT_WORDS if is_product else NORMAL_WORDS
    text = " ".join(random.choices(words, k=4))
    if is_product:
        low, high = random.choice(MOCK_PRICE_RANGES)
        price = random.randint(low, high) * 1000  # به تومان
        text = f"قیمت {price} تومان " + text
    return {
        "post_id": f"post_{idx}",
        "text": text,
        "images": [f"https://img.fake/{idx}.jpg"] if is_product else [],
    }


def fetch_posts(channel, limit: int = 100):
    """
    دریافت پست‌های کانال.
    همیشه اول API ایتا را امتحان می‌کند (نیاز به token ندارد).
    """
    cid = (channel.get("channel_id") or channel.get("id") or "").strip().lstrip("@")
    if cid and " " not in cid:
        try:
            print(f"[Crawler] Fetching posts from Eitaa API: {cid}")
            posts = eitaa_get_posts(channel, limit=limit)
            if posts:
                formatted_posts = []
                for post in posts:
                    formatted_posts.append({
                        "post_id": str(post.get("post_id", "")),
                        "text": post.get("text", ""),
                        "images": post.get("images", []),
                    })
                return formatted_posts
        except Exception as e:
            print(f"[Crawler] API error: {e}")
    
    # Fallback به mock data
    print(f"[Crawler] Using mock data for channel: {channel.get('channel_id')}")
    
    posts = []
    for i in range(random.randint(15, 30)):
        is_product = random.random() > 0.5
        posts.append(fake_post(is_product, i))

    return posts
