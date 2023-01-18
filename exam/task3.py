from msvcrt import kbhit, getch

from threading import Thread, BoundedSemaphore, Event
from time import sleep as slp


class Park(Thread):
    '''Parking interface.'''
    def __init__(
        self, event: Event):
        super().__init__()
        self.stopped = event

    def run(self):
        # While thread is not stopped...
        while not self.stopped.is_set():
            global sema
            try:
                with sema:
                    # ...increasing count of parking busy places.
                    sema.release()
                    print(f'Parked. Count: {sema._value}')
            except ValueError:
                slp(2)
            slp(1)


class Unpark(Thread):
    '''Unparking interface.'''
    def __init__(
        self, event: Event):
        super().__init__()
        self.stopped = event

    def run(self):
        # While thread is not stopped...
        while not self.stopped.is_set():
            global sema
            with sema:
                # ...decreasing count of parking busy places.
                sema.acquire()
                print(f'Unparked. Count: {sema._value}')
            slp(3)


class StopThreads(Thread):
    '''Thread for stopping everyting by pressing ESC button.'''
    def __init__(self, event: Event):
        super().__init__()
        self.event = event

    def run(self):
        while not self.event.is_set():
            # If key is pressed, and key == 'ESC' stopping everything.
            if kbhit() and getch() == b'\x1b':
                self.event.set()


if __name__ == '__main__':
    sema = BoundedSemaphore(10)
    sema._value = 1
    event = Event()

    Park(event).start()
    Unpark(event).start()
    StopThreads(event).start()
