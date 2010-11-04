from distutils.core import setup

mediaExtraFiles = ["*.sql"]

setup(name = "lucidity",
      packages = ['lucidity.media'],
      package_dir = {'lucidity.media' : 'modules/media'},
      package_data = {'lucidity.media' : mediaExtraFiles})