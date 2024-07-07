import time
import math
import cv2 as cv


class TimeCountdown:
    """
    A class to manage and display a countdown timer on a given frame.

    Attributes
    ----------
    total_time : int
        The total countdown time in seconds.
    starting_time : float
        The starting time when the countdown begins.
    """

    def __init__(self, total_time: int):
        """
        Initialize the countdown timer.

        Parameters
        ----------
        total_time : int
            The total countdown time in seconds.
        """
        self.starting_time = time.time()
        self.total_time = total_time

    def display_time(self, frame: cv.Mat) -> bool:
        """
        Display the countdown timer on the given frame.

        Parameters
        ----------
        frame : cv.Mat
            The frame to display the countdown timer on.

        Returns
        -------
        bool
            True if the countdown has ended, else False.
        """
        if self.total_time is None:
            return False
        time_left = self.total_time + math.floor(self.starting_time - time.time())
        if time_left > 0:
            cv.putText(frame, f'Time left: {time_left}', (10, 30), 5, 1, (0, 130, 0), 2)
            return False
        return True
