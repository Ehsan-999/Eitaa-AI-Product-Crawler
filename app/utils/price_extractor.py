import re

def normalize_number(num_str: str) -> int:
    # حذف فاصله
    num_str = num_str.strip()
    
    # حذف جداکننده‌های هزارگان
    num_str = num_str.replace(",", "").replace(".", "")
    
    try:
        return int(num_str)
    except:
        return None


def extract_price(text: str):
    if not text:
        return None

    # تبدیل اعداد فارسی به انگلیسی
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"
    translation_table = str.maketrans(persian_digits, english_digits)
    text = text.translate(translation_table)

    # الگوهای مختلف قیمت
    patterns = [
        r"قیمت\s*[:：]?\s*([\d\.,]+)",
        r"([\d\.,]+)\s*تومان",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            raw_number = match.group(1)
            price = normalize_number(raw_number)
            if price:
                return price

    return None