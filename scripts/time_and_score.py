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
        cv.putText(frame, f'Time left: {self.time_left}', (10, 15), 1, 1, (0, 255, 0), 2)

    def times_up(self):
        return True if self.time_left < 0 else False

    def reset(self, total_time):
        self.starting_time = time.time()
        self.total_time = total_time
        self.time_left = total_time


class ScoreBoard:
    def __init__(self):
        self.score = 0

    def display_score(self, frame):
        cv.putText(frame, f'Score: {self.score}', (10, 30), 1, 1, (0, 255, 0), 2)

    def reset(self):
        self.score = 0

    def __add__(self, score_to_add):
        self.score += score_to_add
