#import audiodevice
#import wave
from lucidity.audiodevice import AudioDeviceList, AudioOutputLoop

if __name__ == "__main__":
    deviceList = AudioDeviceList()
    audioDevice = deviceList.get("Soundflower (2ch)")
    audioOutput = AudioOutputLoop(audioDevice)


    #audioOutput = AudioOutputLoop(44100, 512)
    #audioOutput.start()

    #buffer = ChannelBuffer(1024)
    #audioDevice = AudioDeviceFactory().getAudioDevice()
    #audioDevice.initialize()
    #audioDevice.doStuff(buffer)
    #audioDevice.uninitialize()
    
    #waveFile = wave.open("test.wav", "r")
    #print("File has %d channels, %d frames" % (waveFile.getnchannels(), waveFile.getnframes()))


    #framesRead = 0
    #bufferSize = 512
    #while framesRead < waveFile.getnframes():
    #sampleFrames = waveFile.readframes(bufferSize)
    #buffer.writeData(sampleFrames)
    #framesRead += bufferSize

    #waveFile.close()

