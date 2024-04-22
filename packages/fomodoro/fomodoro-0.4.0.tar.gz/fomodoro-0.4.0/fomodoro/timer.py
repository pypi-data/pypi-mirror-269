"""The timer class."""
from fomodoro.utils import States


class Timer():
    """To can manipulate the timer easiest by functions."""
    def __init__(self) -> None:
        self.state = States.WITHOUT_START
        self.break_time_in_seconds = 0

    def start(self):
        self.state = States.START

    def pause(self):
        self.state = States.PAUSE

    def stop(self):
        self.state = States.STOP
