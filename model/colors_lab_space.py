import numpy as np


class GlobalConstants:
    def __init__(self):
        self.colors = []
        # LAB for cue ball - index 0
        self.colors.append([90, -10, 30])
        # LAB for red balls - index 1
        self.colors.append([30, 35, 30])
        # LAB for yellow balls - index 2
        self.colors.append([80, -10, 80])
        # LAB for green ball - index 3
        self.colors.append([30, -30, 15])
        # LAB for brown ball - index 4
        self.colors.append([35, 5, 40])
        # LAB for blue ball - index 5
        self.colors.append([30, -5, -30])
        # LAB for pink ball - index 6
        self.colors.append([75, 30, 20])
        # LAB for black_ball - index 7
        self.colors.append([10, -15, 10])
        # Convert to regular array
        self.colors = np.array(self.colors)