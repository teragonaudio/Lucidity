from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("audiodevice", ["audiodevice.pyx"], extra_link_args=["-framework", "AudioUnit"])]

setup (
  name = 'audiodevice',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
