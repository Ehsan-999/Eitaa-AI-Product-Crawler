"""
خروجی گرفتن محصولات از دیتابیس و ذخیره در data/products.json
"""
import json
import sys
from pathlib import Path

def main():
    try:
        from app.db.database import SessionLocal
        from app.db.models import Product
    except Exception as e:
        print(f"[!] خطا در اتصال به دیتابیس: {e}")
        return 1

    out_file = Path("data/products.json")
    out_file.parent.mkdir(exist_ok=True)

    db = SessionLocal()
    try:
        rows = db.query(Product).order_by(Product.id.desc()).all()
        products = []
        for r in rows:
            products.append({
                "product_id": r.product_id,
                "channel_id": r.channel_id,
                "text": r.text,
                "price": r.price,
                "image_url": r.image_url,
            })
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"[✓] {len(products)} محصول در {out_file} ذخیره شد.")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(main())
