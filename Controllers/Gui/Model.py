from Entities.ProcessingStrategy import IProcessingStrategy
from Entities.EvaluationStrategy import IEvaluationStrategy

from UseCases.DebugUC import Debug
from UseCases.TestUC import TestUC

from Controllers.CamerController import CV2Controller
class Model:
    allProcessingStrategies: list[IProcessingStrategy]
    allEvaluatingStrategies: list[IEvaluationStrategy]

    processingStrategies: dict[str, IProcessingStrategy]
    evaluationStrategies: dict[str, IEvaluationStrategy]

    def __init__(
            self,
            selectedProcessingStrategies,
            selectedEvaluationStrategies,
            selectedData):
        self.selectedProcessingStrategy = selectedProcessingStrategies
        self.selectedEvaluatingStrategies = selectedEvaluationStrategies
        self.selectedData = selectedData

        self.debugUseCase = Debug(
            CV2Controller(),
            self.selectedProcessingStrategy
        )

        self.testingIsActive = False
        self.testingUseCase = TestUC(
            self.selectedData,
            self.selectedProcessingStrategy,
            self.selectedEvaluatingStrategies
        )
        self.testingIndex = 0

    def getPictureArray(self):
        if not self.testingIsActive:
            return self.debugUseCase.getPictureArray()
        else:
            return self.testingUseCase.getFrameAt(self.testingIndex)

    def setTesting(self, state):
        self.testingIsActive = state

    def setTestingIndex(self, index):
        self.testingIndex = index
