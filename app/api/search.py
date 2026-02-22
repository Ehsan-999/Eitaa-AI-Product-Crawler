from fastapi import APIRouter, Query
from sqlalchemy import text
from app.db.database import SessionLocal
from app.ai.embedding import get_embedding

router = APIRouter()

@router.get("/search")
def search_products(
    q: str = Query(..., description="متن جستجو"),
    min_price: int = None,
    max_price: int = None,
    sort_by: str = Query("relevance", description="relevance یا price"),
    page: int = 1,
    size: int = 10,
):
    """
    جستجوی محصولات با استفاده از vector similarity یا text search
    """
    db = SessionLocal()
    offset = (page - 1) * size

    # تولید embedding برای query
    query_embedding = get_embedding(q)
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    # استفاده از vector similarity اگر embedding موجود باشد
    query_sql = """
    WITH ranked_products AS (
        SELECT *,
               CASE 
                   WHEN embedding IS NOT NULL THEN 
                       1 - (embedding <=> CAST(:embedding AS vector))
                   ELSE 
                       ts_rank(
                           to_tsvector('simple', text),
                           plainto_tsquery('simple', :query)
                       ) / 10.0
               END AS rank
        FROM products
        WHERE (
            embedding IS NOT NULL AND 
            (embedding <=> CAST(:embedding AS vector)) < 1.0
        ) OR (
            embedding IS NULL AND
            to_tsvector('simple', text) @@ plainto_tsquery('simple', :query)
        )
    """

    params = {"query": q, "embedding": embedding_str}

    if min_price:
        query_sql += " AND price >= :min_price"
        params["min_price"] = min_price
    if max_price:
        query_sql += " AND price <= :max_price"
        params["max_price"] = max_price

    query_sql += """
    )
    SELECT *, (SELECT COUNT(*) FROM ranked_products) AS total_count
    FROM ranked_products
    """

    # مرتب‌سازی
    if sort_by == "price":
        query_sql += " ORDER BY price ASC NULLS LAST"
    else:
        query_sql += " ORDER BY rank DESC"

    query_sql += " LIMIT :limit OFFSET :offset"

    params["limit"] = size
    params["offset"] = offset

    try:
        result = db.execute(text(query_sql), params)
        rows = result.fetchall()
        
        if not rows:
            return {"total": 0, "page": page, "size": size, "results": []}

        total = rows[0]._mapping["total_count"]
        
        # تبدیل نتایج به dict و حذف embedding از خروجی
        results = []
        for r in rows:
            row_dict = dict(r._mapping)
            row_dict.pop("embedding", None)  # حذف embedding از خروجی
            results.append(row_dict)

        return {
            "total": total,
            "page": page,
            "size": size,
            "results": results,
        }
    except Exception as e:
        print(f"[API] Search error: {e}")
        # Fallback به text search ساده
        return {"total": 0, "page": page, "size": size, "results": [], "error": str(e)}
    finally:
        db.close()