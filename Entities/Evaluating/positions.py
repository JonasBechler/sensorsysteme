import cv2

from .base import IEvaluationStrategy


class showCurrentPositions(IEvaluationStrategy):
    name = "Current Position"
    dataPoints = 1

    def evaluate(self, img, positions, times):
        position = positions[0]
        if position[0][0] is not None:
            cv2.circle(img, (int(position[0][1]), int(position[0][0])), 5, (0, 0, 255), cv2.FILLED)
        if position[1][0] is not None:
            cv2.circle(img, (int(position[1][1]), int(position[1][0])), 5, (0, 255, 0), cv2.FILLED)
        if position[2][0] is not None:
            cv2.circle(img, (int(position[2][1]), int(position[2][0])), 5, (255, 0, 0), cv2.FILLED)
        return img