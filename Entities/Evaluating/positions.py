import cv2

from .base import IEvaluationStrategy, smoothData, pix2pos


class showCurrentPositions(IEvaluationStrategy):
    name = "Current Position"
    dataPoints = 1

    def evaluate(self, img, positions, times):
        position = positions[0]
        if position[0][0] is not None:
            cv2.circle(img, (int(position[0][1]), int(position[0][0])), 5, (255, 0, 0), cv2.FILLED)
        if position[1][0] is not None:
            cv2.circle(img, (int(position[1][1]), int(position[1][0])), 5, (255, 255, 0), cv2.FILLED)
        if position[2][0] is not None:
            cv2.circle(img, (int(position[2][1]), int(position[2][0])), 5, (0, 0, 255), cv2.FILLED)
        return img


class showAveragePositionsCoordinates(IEvaluationStrategy):
    name = "Smooth(5) Coordinates "
    dataPoints = 5

    def evaluate(self, img, positions, times):
        position = smoothData(positions, 5)
        position = pix2pos(position)
        position = position[0]

        cv2.rectangle(img, (0, 85), (250, 145), (255, 255, 255), -1)
        cv2.rectangle(img, (0, 85), (250, 145), (0, 0, 0), 1)
        for i in range(3):
            if str(position[i][0]) != "nan":
                coordinteStr = "x={:.2f}cm   y={:.2f}cm".format(position[i][1], position[i][0])
                c = (255 if i == 0 else 0,
                     255 if i == 1 else 0,
                     255 if i == 2 else 0)
                cv2.putText(img, coordinteStr, (20, 100 + 20 * i), cv2.FONT_HERSHEY_PLAIN, 1, c, 1)
        return img


class showAveragePositions(IEvaluationStrategy):
    name = "Smooth(5) Position"
    dataPoints = 5

    def evaluate(self, img, positions, times):
        position = smoothData(positions, 5)
        position = position[0]
        # positions = np.array(positions)
        # positions = positions.astype(float)
        # position = np.nanmean(positions, axis=0)

        if str(position[0][0]) != "nan":
            cv2.circle(img, (int(position[0][1]), int(position[0][0])), 5, (255, 0, 0), cv2.FILLED)
        if str(position[1][0]) != "nan":
            cv2.circle(img, (int(position[1][1]), int(position[1][0])), 5, (0, 255, 0), cv2.FILLED)
        if str(position[2][0]) != "nan":
            cv2.circle(img, (int(position[2][1]), int(position[2][0])), 5, (0, 0, 255), cv2.FILLED)
        return img


class showLastNPositions(IEvaluationStrategy):
    name = "Last 50 Positions"
    maxPointSize = 4
    dataPoints = 50

    def evaluate(self, img, positions, times):
        for i in range(self.dataPoints):
            position = positions[i]
            radius = int(self.maxPointSize / self.dataPoints * (self.dataPoints - i))
            if position[0][0] is not None:
                cv2.circle(img, (int(position[0][1]), int(position[0][0])), radius, (255, 0, 0), cv2.FILLED)
            if position[1][0] is not None:
                cv2.circle(img, (int(position[1][1]), int(position[1][0])), radius, (0, 255, 0), cv2.FILLED)
            if position[2][0] is not None:
                cv2.circle(img, (int(position[2][1]), int(position[2][0])), radius, (0, 0, 255), cv2.FILLED)
        return img


class showLastNPositionsSmooth(IEvaluationStrategy):
    name = "Last 50 Smooth(5)"
    maxPointSize = 4
    dataPoints = 50 + 5

    def evaluate(self, img, positions, times):
        positions = smoothData(positions, 5)
        for i in range(self.dataPoints - 5):
            position = positions[i]
            radius = int(self.maxPointSize / self.dataPoints * (self.dataPoints - i))
            if str(position[0][0]) != "nan":
                cv2.circle(img, (int(position[0][1]), int(position[0][0])), radius, (255, 0, 0), cv2.FILLED)
            if str(position[1][0]) != "nan":
                cv2.circle(img, (int(position[1][1]), int(position[1][0])), radius, (0, 255, 0), cv2.FILLED)
            if str(position[2][0]) != "nan":
                cv2.circle(img, (int(position[2][1]), int(position[2][0])), radius, (0, 0, 255), cv2.FILLED)
        return img
