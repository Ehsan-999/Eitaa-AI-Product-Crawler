import os
import random
from app.eitaa.sync_wrapper import get_channel_preview as eitaa_get_preview


SHOP_WORDS = [
    "قیمت",
    "خرید",
    "سفارش",
    "ارسال",
    "فروش",
    "موجود",
    "تومان",
    "پرداخت",
]

NON_SHOP_WORDS = [
    "خبر",
    "سیاسی",
    "آموزش",
    "موزیک",
    "سرگرمی",
    "دانلود",
]


def fake_text(is_shop: bool):
    words = SHOP_WORDS if is_shop else NON_SHOP_WORDS
    return " ".join(random.choices(words, k=10))


def fetch_preview(channel):
    """
    دریافت Bio و چند پست آخر کانال.
    همیشه اول API ایتا را امتحان می‌کند (نیاز به token ندارد).
    """
    cid = (channel.get("channel_id") or channel.get("id") or "").strip().lstrip("@")
    if cid and " " not in cid:
        try:
            print(f"[Preview] Fetching from Eitaa API: {cid}")
            preview = eitaa_get_preview(channel)
            if preview.get("bio") or preview.get("recent_posts"):
                return preview
        except Exception as e:
            print(f"[Preview] API error: {e}")
    
    # Fallback به mock data
    print(f"[Preview] Using mock data for channel: {channel.get('channel_id')}")
    
    # تصادفی بعضی کانال‌ها فروشگاهی هستند
    is_shop_random = random.random() > 0.4

    preview = {
        "channel_id": channel["channel_id"],
        "bio": fake_text(is_shop_random),
        "recent_posts": [fake_text(is_shop_random) for _ in range(5)],
    }

    return preview
