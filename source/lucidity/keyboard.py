from lucidity.log import logger

##+
# Lucidity recognizes the following key commands:
#
# <table border="1">
# <tr><td><b>Key</b><td><b>Operation</b></td></tr>
# <tr><td>Spacebar</td><td>Opens the search window</td></tr>
# <tr><td>Caps Lock</td><td>Turns on/off MIDI mapping mode</td></tr>
# <tr><td>Esc</td><td>Closes any current pop-up window</td></tr>
# <tr><td>Ctrl+P</td><td>Start/Stop playback</td></tr>
# <tr><td>Enter</td><td>Inserts the search selection at the cursor position</td></tr>
# <tr><td>Shift+Enter</td><td>Preview playing at the cursor position</td></tr>
# <tr><td>Ctrl+1</td><td>Inserts the search selection at the cursor position in track 1</td></tr>
# <tr><td>Ctrl+2</td><td>Inserts the search selection at the cursor position in track 2</td></tr>
# <tr><td>Ctrl+3</td><td>Inserts the search selection at the cursor position in track 3</td></tr>
# <tr><td>Ctrl+4</td><td>Inserts the search selection at the cursor position in track 4</td></tr>
# <tr><td>Ctrl+5</td><td>Inserts the search selection at the cursor position in track 5</td></tr>
# <tr><td>Ctrl+6</td><td>Inserts the search selection at the cursor position in track 6</td></tr>
# <tr><td>Ctrl+7</td><td>Inserts the search selection at the cursor position in track 7</td></tr>
# <tr><td>Ctrl+8</td><td>Inserts the search selection at the cursor position in track 8</td></tr>
# <tr><td>Ctrl+9</td><td>Inserts the search selection at the cursor position in track 9</td></tr>
# <tr><td>Ctrl+F</td><td>Fullscreen mode</td></tr>
# <tr><td>Up Arrow</td><td>Moves cursor up, automatically deleting any tracks below the cursor without music or mappings</td></tr>
# <tr><td>Down Arrow</td><td>Moves cursor down, automatically adding a new track if at the bottom of the screen</td></tr>
# <tr><td>Left Arrow</td><td>Moves cursor left, automatically zooming in if at the far right of the screen</td></tr>
# <tr><td>Right Arrow</td><td>Moves cursor right, automatically zooming out if at the far right of the screen</td></tr>
# <tr><td>Shift+Arrow</td><td>Select a region of audio</td></tr>
# <tr><td>Ctrl+Arrow</td><td>Moves the cursor 4x in the given direction</td></tr>
# </table>
#
# Note that the "Ctrl" key listed above also refers to the "Control" key on Mac
# keyboards, not "Command".
#
# Lucidity does not allow the user to remap the key commands.  This is done so that
# the software feels the same on all installations.

RegularKeyCommands = {
}

ControlKeyCommands = {
}

ShiftKeyCommands = {
}

ControlShiftKeyCommands = {
    'q': "quit"
}

ModifierHashes = {
    0: RegularKeyCommands,
    1: ShiftKeyCommands,
    1024: ControlKeyCommands,
    1025: ControlShiftKeyCommands
}

class KeyHandler:
    def processKey(self, delegate, key, modifiers = None):
        keyCharacter = chr(key)
        try:
            if modifiers not in ModifierHashes:
                raise UnhandledModifierError(key, modifiers)
            keyHash = ModifierHashes[modifiers]

            if keyCharacter in keyHash:
                handlerFunction = getattr(delegate, keyHash[keyCharacter])
                handlerFunction()
            else:
                raise UnhandledKeyError(key, modifiers)
        except AttributeError:
            logger.error("Delegate does not handle key command")
        except UnhandledKeyError as error:
            logger.debug("Unhandled command: " + error.printKey())
        except UnhandledModifierError as error:
            logger.debug("Unhandled modifier: " + error.printKey())

class KeyError(Exception):
    def __init__(self, key, modifiers):
        self.key = key
        self.modifiers = modifiers

    def printKey(self):
        return "Key: '" + chr(self.key) + "', Modifiers: " + str(self.modifiers)

class UnhandledKeyError(KeyError):
    pass

class UnhandledModifierError(KeyError):
    pass