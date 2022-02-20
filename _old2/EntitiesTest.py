import queue
import time
import unittest

import TestSamples.SampleAccess
from Controllers.CamerController import CV2Controller
from Entities.PreProcessing import PreProcessing
from Entities.ProcessingStrategy import ProcessingStrategy1


class PreProcessingTests(unittest.TestCase, TestSamples.SampleAccess.SampleAccess):

    def setUp(self):
        self.threads = queue.Queue(maxsize=10)
        self.preP = PreProcessing(self.threads, ProcessingStrategy1(), CV2Controller())

    def testInit(self):
        img, res = self.preP.init()
        location = "ProcessingStrategyInput/x2/"
        self.saveSample(location, (img, res))
        _ = self.loadSamples(location, 2)
        print(self.getFileCount(location))
        self.assertEqual(0, 0)

    def testLoop(self):
        t = self.threads
        self.preP.init()
        startTime = time.time()
        currentTime = time.time()
        for i in range(10):
            startTime, currentTime = self.preP.loop(startTime, currentTime)

        startTime, currentTime = self.preP.loop(startTime, currentTime)

        self.assertEqual(0, 0)

    # def testSomething(self):
    #     for i in range(0, 2):
    #         with self.subTest(i=i):
    #             self.assertEqual(0, 0)

    def tearDown(self):
        pass


class ProcessingTests(unittest.TestCase):

    def setUp(self):
        # self.thread = Processing(None, None, ProcessingStrategy1(), CV2Controller())
        self.preP = PreProcessing(self.thread, ProcessingStrategy1(), CV2Controller())

    def testInit(self):
        res = self.preP.init()
        self.assertEqual(0, 0)

    def testLoop(self):
        pass

    # def testSomething(self):
    #     for i in range(0, 2):
    #         with self.subTest(i=i):
    #             self.assertEqual(0, 0)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
