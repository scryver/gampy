__author__ = 'michiel'

try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

setup(
    name='Gampy',
    version='0.1.0',
    author='M. Schriever',
    author_email='michiel@scryver.com',
    packages=['gampy', 'gampy.engine', 'gampy.engine.render', 'gampy.engine.events',
              'gampy.engine.input', 'gampy.engine.objects', 'gampy.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/Gampy/',
    license='LICENSE.txt',
    description='A simple 3D game engine.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyOpenGL >= 3.1.0",
        "numpy >= 1.11.0",
        "pillow >= 3.2.0",
    ],
)
