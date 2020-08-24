# Scheduling Job
from threading import Thread
import datetime


class scheduled:

    def __init__(self, wait, func, arg=None):
        self.wait = wait
        self.func = func
        self.arg = arg
        self.thread = Thread(target=self.scheduler, args=(self.wait, self.func, self.arg))

    @staticmethod
    def scheduler(wait, func, arg):
        previusTime = 0
        while True:
            currentTime = datetime.datetime.now().hour
            if (currentTime - previusTime) >= wait:
                previusTime = currentTime
                if arg is not None:
                    func(arg)
                else:
                    func()

    def start(self):
        self.thread.start()
