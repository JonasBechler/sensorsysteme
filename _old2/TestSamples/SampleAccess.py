import os
import pickle
import time


class SampleAccess:
    def getFileCount(self, folder):
        filesNames = os.listdir("./TestSamples/" + folder)
        return len(filesNames)

    def saveSample(self, folder, data):
        folderPath = "TestSamples/" + folder
        path = folderPath + time.strftime("%Y-%m-%d-%H:%M") + ".pckl"
        with open(path, "wb") as f:
            pickle.dump(data, f)
            f.close()

    def loadSamples(self, folder, n):
        folderPath = "TestSamples/" + folder
        filesNames = os.listdir("./TestSamples/" + folder)
        filesNames.reverse()
        nMax = len(filesNames)
        if n > nMax:
            print("more samples needed")
            return None

        retval = [None]*n
        for i, filesName in enumerate(filesNames):
            if i >= n:
                return retval
            path = folderPath + filesName

            with open(path, "rb") as f:
                retval[i] = pickle.load(f)

        return None
