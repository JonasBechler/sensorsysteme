import cv2
import numpy as np

from .base import IEvaluationStrategy, smoothData, pix2pos, map


class speedUpDownTimes(IEvaluationStrategy):
    name = "UpDown Times"
    dataPoints = 150 + 4

    def evaluate(self, img, positions, times):
        def checkTimeUpDown(positions, times):
            index = 0
            testing = times[0] is None
            try:
                while positions[index][1] <= 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                index = index + 5
                while positions[index][1] > 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                timeBefore60cm_first = times[index]
                if testing:
                    timeBefore60cm_first = index
                index = index + 5

                while positions[index][1] <= 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                index = index + 5
                while positions[index][1] > 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                timeBefore60cm_second = times[index]
                if testing:
                    timeBefore60cm_second = index
            except Exception as e:
                return None

            deltaT = timeBefore60cm_first - timeBefore60cm_second
            if testing:
                deltaT = -deltaT * 1 / 30
            return deltaT

        positions = smoothData(positions, 5)
        positions = pix2pos(positions)
        positions = np.array(positions)

        cv2.rectangle(img, (0, 145), (250, 205), (255, 255, 255), -1)
        cv2.rectangle(img, (0, 145), (250, 205), (0, 0, 0), 1)
        for i in range(3):
            deltaT = checkTimeUpDown(positions[:, i], times)
            if deltaT is not None:
                deltaTStr = "deltaT = {:.2f}s".format(deltaT)
                c = (255 if i == 0 else 0,
                     255 if i == 1 else 0,
                     255 if i == 2 else 0)
                cv2.putText(img, deltaTStr, (20, 160 + 20 * i), cv2.FONT_HERSHEY_PLAIN, 1, c, 1)
        return img


class speedUpDownScore(IEvaluationStrategy):
    name = "UpDown Speed Score"
    dataPoints = 150 + 4

    def evaluate(self, img, positions, times):
        def checkTimeUpDown(positions, times):
            index = 0
            testing = times[0] is None
            try:
                while positions[index][1] <= 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                index = index + 5
                while positions[index][1] > 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                timeBefore60cm_first = times[index]
                if testing:
                    timeBefore60cm_first = index
                index = index + 5

                while positions[index][1] <= 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                index = index + 5
                while positions[index][1] > 60 or str(positions[index][1]) == "nan":
                    index = index + 1
                timeBefore60cm_second = times[index]
                if testing:
                    timeBefore60cm_second = index
            except Exception as e:
                return None

            deltaT = timeBefore60cm_first - timeBefore60cm_second
            if testing:
                deltaT = -deltaT * 1 / 30
            return deltaT

        positions = smoothData(positions, 5)
        positions = pix2pos(positions)
        positions = np.array(positions)

        timeCount = 0
        time = 0
        for i in range(3):
            deltaT = checkTimeUpDown(positions[:, i], times)
            if deltaT is not None:
                timeCount = timeCount + 1
                time = time + deltaT

        if timeCount == 0:
            score = 0
        else:
            time = time / 3
            if time > 4:
                score = 0
            elif time > 1:
                score = map(time, 1, 4, 500, 0)
            elif time >= .5:
                score = map(time, 1, .5, 500, 1000)
            else:
                score = 1000

        scoreStr = f"Speed Score: {int(score)}Pkt"
        cv2.rectangle(img, (880, 0), (1279, 35), (255, 255, 255), -1)
        cv2.rectangle(img, (880, 0), (1279, 35), (0, 0, 0), 1)
        cv2.putText(img, scoreStr, (900, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        return img


class straightScore(IEvaluationStrategy):
    name = "Straight Score"
    dataPoints = 50 + 4

    tolerance = 100

    def evaluate(self, img, positions, times):
        def checkStraightness(positions):
            positionCount = len(positions) - np.count_nonzero(np.isnan(positions[:, 0]))
            maxX = np.nanmax(positions[:, 0])
            minX = np.nanmin(positions[:, 0])

            maxY = np.nanmax(positions[:, 1])
            minY = np.nanmin(positions[:, 1])
            if positionCount < 5 or maxY - minY < 25:
                return None
            return maxX - minX

        positions = smoothData(positions, 5)
        positions = pix2pos(positions)
        positions = np.array(positions)

        count = 0
        distance = 0
        score = 0
        for i in range(3):
            distanceOneColor = checkStraightness(positions[:, i])
            if distanceOneColor is not None:
                count = count + 1
                distance = distance + distanceOneColor

        if count == 0:
            score = 0
        else:
            distance = distance / count
            if distance > 80:
                score = 0
            elif distance > 5:
                score = map(distance, 5, 80, 1000, 0)
            elif distance <= 5:
                score = 1000
        scoreStr = f"Accurateness: {int(score)}Pkt"
        cv2.rectangle(img, (880, 35), (1279, 65), (255, 255, 255), -1)
        cv2.rectangle(img, (880, 35), (1279, 65), (0, 0, 0), 1)
        cv2.putText(img, scoreStr, (900, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        return img
