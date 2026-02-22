import time


class Backoff:
    def __init__(self, base_delay=1, max_delay=60):
        self.base = base_delay
        self.max = max_delay
        self.attempt = 0

    def fail(self):
        self.attempt += 1
        delay = min(self.base * (2 ** self.attempt), self.max)
        print(f"[Backoff] sleeping {delay}s بسبب rate limit...")
        time.sleep(delay)

    def success(self):
        self.attempt = 0
