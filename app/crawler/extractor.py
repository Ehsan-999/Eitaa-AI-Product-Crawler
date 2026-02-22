from app.utils.price_extractor import extract_price


def extract_product(post: dict, channel_id: str):
    price = extract_price(post["text"])

    product = {
        "product_id": f"{channel_id}_{post['post_id']}",
        "channel_id": channel_id,
        "text": post["text"],
        "price": price,
        "images": post["images"],
    }

    return product
