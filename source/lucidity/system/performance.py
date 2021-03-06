import os
from psutil import Process
from threading import Thread
from lucidity.system.status import StatusProvider

class SystemUsageLoop(Thread, StatusProvider):
    def __init__(self, pollIntervalInSec=1.0):
        Thread.__init__(self, name="SystemUsage")
        self.delegate = None
        self.fpsProvider = None
        self._pollInterval = pollIntervalInSec
        self._isRunning = False
        self.cpuUsage = 0.0
        self.memUsage = 0.0

    def getStatusString(self):
        memUsedInMb = round(self.memUsage / (1024 * 1024), 2)
        fps = round(self.fpsProvider.getFramesPerSec(), 1)
        return "CPU: %g%%, Mem: %gMb, FPS: %g" % (self.cpuUsage, memUsedInMb, fps)

    def quit(self):
        self._isRunning = False

    def run(self):
        self._isRunning = True
        process = Process(os.getpid())
        while self._isRunning:
            self.cpuUsage = process.get_cpu_percent(self._pollInterval)
            self.memUsage = process.get_memory_info()[0]
            if self.delegate is not None:
                self.delegate.processCpuUsage(self.cpuUsage)
                self.delegate.processMemUsage(self.memUsage)
