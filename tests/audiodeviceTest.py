#import audiodevice
#import wave
from audiodevice import ChannelBuffer, AudioDeviceFactory

if __name__ == "__main__":
    buffer = ChannelBuffer(1024)
    audioDevice = AudioDeviceFactory().getAudioDevice()
    audioDevice.initialize()
    #audioDevice.doStuff(buffer)
    
    #waveFile = wave.open("test.wav", "r")
    #print("File has %d channels, %d frames" % (waveFile.getnchannels(), waveFile.getnframes()))


    #framesRead = 0
    #bufferSize = 512
    #while framesRead < waveFile.getnframes():
    #sampleFrames = waveFile.readframes(bufferSize)
    #buffer.writeData(sampleFrames)
    #framesRead += bufferSize

    #waveFile.close()
