from lucidity.system.log import logger
from lucidity.app.keyboard import KeyHandler

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
class MainDelegate:
    def __init__(self, mainWindow:"MainWindow"):
        self.mainWindow = mainWindow
        self.mainGrid = None
        self.keyHandler = KeyHandler()

    def onCue(self):
        pass

    def onMoveLeft(self):
        self.mainGrid.moveLeft()

    def onMoveRight(self):
        self.mainGrid.moveRight()

    def onMoveUp(self):
        self.mainGrid.moveUp()

    def onMoveDown(self):
        self.mainGrid.moveDown()

    def onActiveEvent(self, eventDict):
        gain = eventDict['gain']
        state = eventDict['state']
        logger.info("Application activated, gain: " + str(gain) + ", state: " + str(state))

    def onKeyDown(self, eventDict):
        self.keyHandler.onKeyDown(self, eventDict['key'], eventDict['mod'])

    def onKeyUp(self, eventDict):
        self.keyHandler.onKeyUp(self, eventDict['key'], eventDict['mod'])

    def onMouseButtonDown(self, eventDict):
        self.mainWindow.onMouseButtonDown(eventDict)

    def onMouseButtonUp(self, eventDict):
        self.mainWindow.onMouseButtonUp(eventDict)

    def onMouseMotion(self, eventDict):
        pass

    def onMinimize(self, eventDict = None):
        self.mainWindow.minimize()

    def onQuit(self, eventDict = None):
        self.mainWindow.quit()

    def onUndo(self):
        pass

    def onRedo(self):
        pass

    def onSelect(self):
        pass

    def onDelete(self):
        pass

    def onClone(self):
        pass

    def onSave(self):
        pass

    def onSettings(self):
        pass

    def onReset(self):
        logger.info("Reset called")
        self.mainGrid.reset()