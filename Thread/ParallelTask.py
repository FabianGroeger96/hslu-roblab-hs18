from threading import Thread

class ParallelTask:
    runable = None
    thread = None
    isRunning = False

    def __init__(self, runable):
        self.runable = runable
        self.thread = Thread(target=self.runable.Run)

    def Start(self):
        if not self.isRunning:
            self.isRunning = True
            self.thread.start()

    def Stop(self):
        self.runable.Stop()
        self.isRunning = False