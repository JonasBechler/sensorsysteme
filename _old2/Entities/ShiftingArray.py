class ShiftingArray:
    def __init__(self, objectT, maxCount=10):
        self.maxCount = maxCount
        self.elementCount = 0
        self.elements = [objectT] * maxCount

    def get(self):
        return self.elements

    def push(self, element):
        del self.elements[self.maxCount - 1]
        self.elements.append(None)

        for i in range(self.maxCount - 1):
            self.elements[self.maxCount - i - 1] = self.elements[self.maxCount - i - 2]
        self.elements[0] = element
        self.elementCount = self.elementCount + 1

    def full(self):
        if self.maxCount < self.elementCount:
            return True
        else:
            return False
