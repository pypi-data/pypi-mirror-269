"""The stopwatch class."""
from fomodoro.utils import States


class Stopwatch():
    """To can manipulate the stopwatch easiest by functions."""
    def __init__(self) -> None:
        self.state = States.WITHOUT_START
        self.elapsed_seconds = 0
        self.seconds = 0

    def start(self):
        self.state = States.START

    def pause(self):
        self.state = States.PAUSE

    def stop(self):
        self.state = States.STOP
