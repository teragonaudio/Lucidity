from distutils.core import setup, Extension

setup(name = "audioDevice", version = "1.0",
      ext_modules = [Extension("audioDevice",
                               ["ChannelBuffer.c"])])
