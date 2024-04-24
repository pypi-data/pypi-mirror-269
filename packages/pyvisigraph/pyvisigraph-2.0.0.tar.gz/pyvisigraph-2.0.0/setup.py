from setuptools import setup

with open('requirements.txt', 'r') as fr:
  required = fr.read().splitlines()
  
setup(
  name = 'pyvisigraph',
  packages = ['pyvisigraph'],
  version = '2.0.0',
  description = 'Given a set of simple obstacle polygons, build a visibility graph and find the shortest path between two points.',
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  author = 'Vincent Laffargue',
  author_email = 'vincent.laffargue@gmail.com',
  url = 'https://github.com/pingou2712/pyvisigraph',
  download_url = 'https://github.com/pingou2712/pyvisigraph/tarball/2.0.0',
  install_requires = required,
  keywords = ['visibility', 'graph', 'shortest'],
  classifiers = [],
)
