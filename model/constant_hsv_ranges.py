from model import boundaries_pair as bp
import numpy as np


class GlobalConstants:
    def __init__(self):
        self.bounds = []
        # HSV boundaries for cue ball - index 0
        self.bounds.append(bp.BoundariesPair([25, 0, 215], [180, 120, 255]))
        # HSV boundaries for red balls - index 1
        self.bounds.append(bp.BoundariesPair([0, 180, 50], [15, 255, 255]))
        # HSV boundaries for yellow balls - index 2
        self.bounds.append(bp.BoundariesPair([20, 180, 160], [40, 255, 255]))
        # HSV boundaries for green ball - index 3
        self.bounds.append(bp.BoundariesPair([65, 100, 70], [90, 255, 255]))
        # HSV boundaries for brown ball - index 4
        self.bounds.append(bp.BoundariesPair([10, 170, 40], [30, 255, 160]))
        # HSV boundaries for blue ball - index 5
        self.bounds.append(bp.BoundariesPair([85, 180, 40], [120, 255, 255]))
        # HSV boundaries for pink ball - index 6
        self.bounds.append(bp.BoundariesPair([0, 0, 140], [25, 150, 255]))
        # HSV boundaries for black_ball - index 7
        self.bounds.append(bp.BoundariesPair([55, 0, 0], [180, 255, 50]))
        # HSV boundaries for table ( cloth ) - index 8
        self.bounds.append(bp.BoundariesPair([30, 140, 0], [75, 255, 255]))
        # Convert to regular array
        self.bounds = np.array(self.bounds)
