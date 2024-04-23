from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='DeFiPie',
      version='0.0.1',
      description='DeFiPie',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/icmoore/defipie',
      author = "icmoore",
      author_email = "defipy.devs@gmail.com",
      license='MIT',
      package_dir = {"defipie": "python/prod"},
      packages=[
          'defipie',
          'defipie.erc'
      ],   
      zip_safe=False)
