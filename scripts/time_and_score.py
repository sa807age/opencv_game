import time
import math
import cv2 as cv


class TimeCountdown:
    def __init__(self, total_time):
        self.starting_time = time.time()
        self.total_time = total_time
        self.time_left = total_time

    def display_time(self, frame):
        self.time_left = self.total_time + math.floor(self.starting_time - time.time())
        cv.putText(frame, f'Time left: {self.time_left}', (10, 30), 4, 1, (0, 130, 0), 2)
        return True if self.time_left < 1 else False
