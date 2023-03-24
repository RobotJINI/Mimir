from gpiozero import Button
from threading import Thread, Lock
import time


class ButtonSensor(Thread):
    def __init__(self, button):
        Thread.__init__(self)
        self._running = False
        self._count = 0
        self._start_time = 0
        self._mutex = Lock()
        self._sensor = Button(button)
        
    def run(self):
        self._start_time = self._get_time()
        self._sensor.when_pressed = self._spin
        self._running = True
        while self._running:
            time.sleep(.1)

    def stop(self):
        self._running = False
        
    def update(self):
        raise NotImplementedError('call to abstract method update in ButtonSensor')
    
    def _spin(self):
        self._mutex.acquire()
        self._count += 1
        self._mutex.release()
    
    def _get_and_reset(self):
        self._mutex.acquire()
        
        #Get
        count = self._count
        start_time = self._start_time
        
        #Reset
        self._count = 0
        self._start_time = self._get_time()
        end_time = self._start_time
        
        self._mutex.release()
        
        interval_sec = end_time - start_time
        
        return (count, interval_sec)
        
    def _get_time(self):
        return time.time()
