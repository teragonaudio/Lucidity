from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import sys

platformLinkArgs = []

if sys.platform == "darwin":
    platformLinkArgs = ['-framework', 'AudioUnit']

setup(name = "lucidity",
      cmdclass = {'build_ext': build_ext},
      packages = [
          'lucidity',
          'id3reader'
          ],
      package_dir = {
          'lucidity': 'source/lucidity',
          'id3reader': 'third-party/id3reader'
          },
      package_data = {
          'lucidity': ["*.sql"]
          },
      ext_modules = [
          Extension("lucidity.audiodevice",
                    ["source/lucidity/audiodevice.py"],
                    extra_link_args = platformLinkArgs)
          ],
      )
