SHOP_KEYWORDS = [
    "قیمت",
    "خرید",
    "سفارش",
    "ارسال",
    "فروش",
    "موجود",
    "تومان",
    "پرداخت",
]


def is_shop_channel(preview: dict):
    text = preview["bio"] + " " + " ".join(preview["recent_posts"])

    score = 0
    for word in SHOP_KEYWORDS:
        if word in text:
            score += 1

    # threshold ساده
    is_shop = score >= 3

    return {
        "channel_id": preview["channel_id"],
        "is_shop": is_shop,
        "score": score,
    }
