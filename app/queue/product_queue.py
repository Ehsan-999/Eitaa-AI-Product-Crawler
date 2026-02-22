from rq import Queue
from app.queue.redis_conn import redis_conn

product_queue = Queue("products", connection=redis_conn)
