import itertools
import random


class SessionManager:
    def __init__(self, sessions: list[str]):
        self.sessions = sessions
        random.shuffle(self.sessions)
        self._cycle = itertools.cycle(self.sessions)

    def get_session(self):
        """
        هر بار یک session متفاوت می‌دهد (round robin)
        """
        return next(self._cycle)
