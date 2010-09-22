    from distutils.core import setup, Extension

    setup(name = "audioDevice",
          version = "1.0",
          author = "Teragon Audio",
          ext_modules = [Extension("audiodevice",
                                   ["AudioDevice.c",
                                    "ChannelBuffer.c",
                                    "AudioOutputOSX.c"])])
