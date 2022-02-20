import queue

from PostProcessing import PostProcessing
from PreProcessing import PreProcessing

if __name__ == '__main__':
    threads = queue.Queue(maxsize=10)

    preThread = PreProcessing(threads, targetFps=30,
                              resizeDivider=32, strengthThreshold=[100, 100, 100], countThreshold=[5, 5, 5])
    postThread = PostProcessing(threads, maxCount=50)
    preThread.start()
    postThread.run()
