from lucidity.log import logger
from lucidity.keyboard import KeyHandler

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
class MainDelegate:
    def __init__(self, mainWindow:"MainWindow"):
        self.mainWindow = mainWindow
        self.mainGrid = None
        self.keyHandler = KeyHandler()

    def processCue(self):
        pass

    def processMoveLeft(self):
        self.mainGrid.moveLeft()

    def processMoveRight(self):
        self.mainGrid.moveRight()

    def processMoveUp(self):
        self.mainGrid.moveUp()

    def processMoveDown(self):
        self.mainGrid.moveDown()

    def processActiveEvent(self, eventDict):
        gain = eventDict['gain']
        state = eventDict['state']
        logger.info("Application activated, gain: " + str(gain) + ", state: " + str(state))

    def processKeyDown(self, eventDict):
        self.keyHandler.processKeyDown(self, eventDict['key'], eventDict['mod'])

    def processKeyUp(self, eventDict):
        self.keyHandler.processKeyUp(self, eventDict['key'], eventDict['mod'])

    def processMouseButtonDown(self, eventDict):
        self.mainWindow.processMouseButtonDown(eventDict)

    def processMouseButtonUp(self, eventDict):
        self.mainWindow.processMouseButtonUp(eventDict)

    def processMouseMotion(self, eventDict):
        pass

    def processMinimize(self, eventDict = None):
        self.mainWindow.minimize()

    def processQuit(self, eventDict = None):
        self.mainWindow.quit()

    def processUndo(self):
        pass

    def processRedo(self):
        pass

    def processSelect(self):
        pass

    def processDelete(self):
        pass

    def processClone(self):
        pass

    def processSave(self):
        pass

    def processSettings(self):
        pass

    def processReset(self):
        logger.info("Reset called")
        self.mainGrid.reset()