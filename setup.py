from setuptools import setup

with open("README.md", "r") as f:
  _long_description = f.read()


setup(
  name = 'unknownfiles',
  packages = ['unknownfiles'],
  version = '0.0.1',
  license='GNU General Public License Version 3',
  description = 'Wrapper around the anonfiles.com API',
  long_description = _long_description,
  long_description_content_type='text/markdown',
  author = 'Aaron Levi Can (aaronlyy)',
  url = 'https://github.com/aaronlyy/unknownfiles',
  download_url = 'https://github.com/aaronlyy/unknownfiles/archive/v0.0.1.tar.gz',
  keywords = ['api', 'wrapper', 'files', 'hosting', 'filehosting'],
  install_requires=[
        "requests",
      ],
)