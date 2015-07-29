__author__ = 'michiel'

from setuptools import setup

setup(
    name='Gampy',
    version='0.1.0',
    author='M. Schriever',
    author_email='michiel@scryver.com',
    packages=['gampy', 'gampy.engine', 'gampy.engine.render', 'gampy.engine.events',
              'gampy.engine.input', 'gampy.engine.objects', 'gampy.test'],
    scripts=[],
    url='https://github.com/scryver/gampy',
    license='LICENSE.txt',
    description='A simple 3D game engine.',
    long_description=open('README.md').read(),
    install_requires=[
        "PyOpenGL >= 3.1.0",
        "PySDL2 >= 0.9.3",
    ],
)
