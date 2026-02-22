from rq import Queue
from rq.worker import SimpleWorker

from app.queue.redis_conn import redis_conn

listen = ["products"]

if __name__ == "__main__":
    queues = [Queue(name, connection=redis_conn) for name in listen]

    worker = SimpleWorker(queues, connection=redis_conn)

    print("[Worker] started in SIMPLE mode (no fork, Windows compatible)")
    worker.work()
