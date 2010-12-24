import os
from psutil import Process
from threading import Thread

class SystemUsage(Thread):
    def __init__(self, delegate, pollIntervalInSec=1):
        Thread.__init__(self, name="SystemUsage")
        self.delegate = delegate
        self._pollInterval = pollIntervalInSec
        self._isRunning = False

    def quit(self):
        self._isRunning = False

    def run(self):
        self._isRunning = True
        process = Process(os.getpid())
        while self._isRunning:
            cpuUsage = process.get_cpu_percent(self._pollInterval)
            memUsage = process.get_memory_info()
            self.delegate.processCpuUsage(cpuUsage)
            self.delegate.processMemUsage(memUsage[0])
