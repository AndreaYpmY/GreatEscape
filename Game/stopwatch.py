import time

# Singleton class
class Stopwatch:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.start_time = None
            cls._instance.elapsed_time = 0
        return cls._instance

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.start_time is not None:
            return self.elapsed_time + (time.time() - self.start_time)
        else:
            return self.elapsed_time