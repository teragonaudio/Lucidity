from distutils.core import setup

setup(name = "lucidity",
      packages = [
          'lucidity',
          'lucidity.media',
          'id3reader'
          ],
      package_dir = {
          'lucidity': 'source/modules',
          'lucidity.media': 'source/modules/media',
          'id3reader': 'third-party/id3reader'
          },
      package_data = {
          'lucidity.media': ["*.sql"]
          }
      )
