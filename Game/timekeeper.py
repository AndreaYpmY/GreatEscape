import time

# Singleton class
class Timekeeper:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.start_time = None
            cls._instance.MAX_TURN_DURATION_SECONDS = 1 # TODO: Per adesso 1s, poi andrà cambiato in base al tempo che ci mette l'AI a generare la mossa

        return cls._instance

    def start(self):
        self.start_time = time.time()

    def get_start_time(self):
        if self.start_time is not None:
            return self.start_time
        return 0