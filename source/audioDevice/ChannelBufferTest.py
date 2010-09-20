__author__ = 'nik'

from audioDevice import ChannelBuffer
import wave

if __name__ == "__main__":
    waveFile = wave.open("test.wav", "r")
    print("File has %d channels, %d frames" % (waveFile.getnchannels(), waveFile.getnframes()))

    buffer = ChannelBuffer(1024)

    framesRead = 0
    bufferSize = 512
    #while framesRead < waveFile.getnframes():
    sampleFrames = waveFile.readframes(bufferSize)
    buffer.writeData(sampleFrames)
    framesRead += bufferSize

    waveFile.close()
    