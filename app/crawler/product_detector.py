from app.utils.price_extractor import extract_price

MIN_TEXT_LENGTH = 20

def is_product_post(post: dict, keyword: str = None) -> bool:
    text = post.get("text", "").strip()

    if not text or len(text) < MIN_TEXT_LENGTH:
        return False

    # باید قیمت داشته باشد
    price = extract_price(text)
    if price is None:
        return False

    # اگر keyword داده شده باشد
    if keyword:
        if keyword not in text:
            return False

    # حذف پست‌های تبلیغ کانال
    if "joinchat" in text.lower():
        return False

    return True