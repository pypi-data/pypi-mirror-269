from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='DeFiPi',
      version='0.0.1',
      description='DeFiPi',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/icmoore/defipi',
      author = "icmoore",
      author_email = "defipy.devs@gmail.com",
      license='MIT',
      package_dir = {"defipi": "python/prod"},
      packages=[
          'defipi',
          'defipi.erc'
      ],   
      zip_safe=False)
