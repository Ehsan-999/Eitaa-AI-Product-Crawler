from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True, index=True)
    channel_id = Column(String)
    text = Column(Text)
    price = Column(Integer)
    sizes = Column(JSON, nullable=True)
    colors = Column(JSON, nullable=True)
    material = Column(String, nullable=True)
    has_image = Column(Integer, default=0)
    image_url = Column(String)

    embedding = Column(Vector(1536))  # 🔥 اضافه شد