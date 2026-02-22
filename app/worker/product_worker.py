from app.utils.price_extractor import extract_price
from app.db.models import Product
from app.db.database import SessionLocal
from app.ai.embedding import get_embedding
from app.ai.product_entity_extractor import extract_entities

def process_product(product: dict):
    """
    پردازش محصول و ذخیره در دیتابیس
    این تابع توسط RQ Worker فراخوانی می‌شود
    """
    db = SessionLocal()
    
    try:
        # جلوگیری از duplicate
        existing = db.query(Product).filter_by(
            product_id=product["product_id"]
        ).first()

        if existing:
            print(f"[Worker] Product {product['product_id']} already exists, skipping")
            return
        
        # تولید embedding
        embedding = get_embedding(product["text"])
        
        # استخراج قیمت (اگر در product موجود نباشد)
        price = product.get("price")
        if price is None:
            price = extract_price(product["text"])
        # محدوده INTEGER دیتابیس؛ در غیر این صورت ذخیره نکن
        if price is not None and (price < 0 or price > 2_147_483_647):
            price = None
        entities = extract_entities(product["text"])
        db_product = Product(
            embedding=embedding,
            sizes=entities.get("sizes"),
            colors=entities.get("colors"),
            material=entities.get("material"),
            has_image=1 if product.get("images") else 0,
            product_id=product["product_id"],
            channel_id=product["channel_id"],
            text=product["text"],
            price=price,
            image_url=product["images"][0] if product.get("images") else None,
        )

        db.add(db_product)
        db.commit()
        print(f"[Worker] Product {product['product_id']} saved successfully")
        
    except Exception as e:
        db.rollback()
        print(f"[Worker] Error processing product {product.get('product_id', 'unknown')}: {e}")
        raise
    finally:
        db.close()