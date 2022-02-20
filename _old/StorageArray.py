from Processing import Processing


class StorageArray:
    def __init__(self, maxCount=10):
        self.maxCount = maxCount
        self.elementCount = 0
        self.elements = [Processing] * maxCount

    def at(self, i):
        if type(i) == list:
            ret = []
            for j in range(len(i)):
                ret[j] = self.elementAt(i[j])
            return ret

        else:
            return self.elementAt(i)

    def elementAt(self, i):
        if i < 0:
            i = i * -1
        if i < self.maxCount:
            return self.elements[i]
        return None

    def push(self, element):
        for i in range(self.maxCount - 1):
            self.elements[self.maxCount - i - 1] = self.elements[self.maxCount - i - 2]
        self.elements[0] = element

    def full(self):
        if self.maxCount < self.elementCount:
            return True
        else:
            return False
