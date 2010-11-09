from lucidity.midi import MidiEventLoop
from time import sleep

if __name__ == "__main__":
    midiEventLoop = MidiEventLoop()
    midiEventLoop.start()
    midiEventLoop.devices.openInput('UC-33 USB MIDI Controller Port 1')
    sleep(5)
    midiEventLoop.terminate()
    print("MIDI system closed")