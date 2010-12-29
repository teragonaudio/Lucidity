from lucidity.system.log import logger
from lucidity.app.keyboard import KeyHandler

# Avoid warnings about unused locals, which is necessary for the event handlers to work
# properly via reflection
#noinspection PyUnusedLocal
from lucidity.system.platforms import Naming

class MainDelegate:
    """This class serves as the main dispatcher point for the application.  The primary
    objects in the app, such as the main window, grid, and app must register themselves
    in this class in order to receive notifications about particular events.

    Events from the keyboard, mouse, and MIDI devices are processed through this class
    and sent to the respective classes which handle those events.
    """
    def __init__(self):
        self.mainApp = None
        self.mainWindow = None
        self.mainGrid = None
        self.keyHandler = KeyHandler()
        self.popupActive = False

    def onCue(self):
        """Play the audio directly under the cursor point out of the cue output"""
        pass

    def onMoveLeft(self):
        """Move the cursor to the left"""
        self.mainGrid.moveLeft()

    def onMoveRight(self):
        """Move the cursor to the right"""
        self.mainGrid.moveRight()

    def onMoveUp(self):
        """Move the cursor up"""
        self.mainGrid.moveUp()

    def onMoveDown(self):
        """Move the cursor down"""
        self.mainGrid.moveDown()

    def onActiveEvent(self, eventDict):
        """Called when the application window enters the foreground"""
        gain = eventDict['gain']
        state = eventDict['state']
        logger.info("Application activated, gain: " + str(gain) + ", state: " + str(state))

    def onKeyDown(self, eventDict):
        """Key pressed.  Note that key repeat is NOT supported by the underlying
        frameworks here.  This event is only sent once for each key.  Also note that
        a keyboard is not a multitouch device -- it is capable of only sending a single
        keystroke at a time.
        """
        key = eventDict['key']
        modifiers = eventDict['mod']

        if modifiers:
            # Always process control keys
            self.keyHandler.onKeyDown(self, key, modifiers)
        elif self.popupActive:
            # Escape pressed -- hide the popup
            if key == 27:
                self.mainGrid.hidePopup()
                self.popupActive = False
            else:
                # TODO: Send key to popup
                pass
        else:
            self.keyHandler.onKeyDown(self, key, modifiers)

    def onKeyUp(self, eventDict):
        """Key released"""
        pass

    def onMouseButtonDown(self, eventDict):
        """Mouse button pressed"""
        self.mainWindow.onMouseButtonDown(eventDict)

    def onMouseButtonUp(self, eventDict):
        """Mouse button released"""
        self.mainWindow.onMouseButtonUp(eventDict)

    def onMouseMotion(self, eventDict):
        """Mouse moved (ignored)"""
        pass

    def onMinimize(self, eventDict = None):
        """Main window called to minimize"""
        self.mainWindow.minimize()

    def onQuit(self, eventDict = None):
        """Application asked to quit"""
        self.mainApp.quit()

    def onQuitHelp(self, eventDict = None):
        self.mainWindow.setStatusText("Press %s + shift + Q to quit" % Naming.commandKeyName())

    def onUndo(self):
        """Undo the last cursor edit"""
        pass

    def onRedo(self):
        """Redo the last cursor edit"""
        pass

    # TODO: This should probably be onSelectDown and onSelectUp
    def onSelect(self):
        pass

    def onDelete(self):
        """Delete the item directly under the cursor"""
        pass

    def onClone(self):
        """Make a copy of the item directly under the cursor directly after the item"""
        pass

    # TODO: Rename feature to "bounce"
    def onSave(self):
        """Bounce the selection under the cursor to a new file"""
        pass

    def onSettings(self):
        """Open the settings window"""
        pass

    def onSearch(self):
        """Open the search window"""
        self.mainGrid.showSearchPopup()
        self.popupActive = True

    def onInsert(self):
        """Insert the currently selected media file into the arrangement under the cursor"""
        self.mainWindow.insert()

    # TODO: Split into onStartMidiMapping/onStopMidiMapping
    def onMapMidi(self):
        pass

    def onReset(self):
        """Remove all items from the arrangement"""
        logger.info("Reset called")
        self.mainGrid.reset()