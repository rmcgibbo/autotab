from setuptools import setup

setup(name='autotab',
      version='0.1',
      description='Numpy docstring autotab for IPython',
      author='Robert McGibbon',
      author_email='rmcgibbo@gmail.com',
      py_modules = ['autotab'],
      install_requires=['numpydoc'],
     )