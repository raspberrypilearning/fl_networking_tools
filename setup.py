from setuptools import setup

__project__ = "fl_networking_tools"
__version__ = "0.0.1"
__description__ = "A set of tools for use with the FutureLearn Programming with networks course from Raspberry Pi"
__packages__ = ["fl_networking_tools"]
__author__ = "The Raspberry PI Foundation"
__author_email__ = "mac@raspberrypi.org"
__classifiers__ = [
	"Development Status :: 3 - Alpha",
	"Intended Audience :: Education",
	"Programming Language :: Python :: 3",
]
__keywords__ = [
	"Networking", 
	"Education",
	"FutureLearn", 
	"Binary",
	"ImageViewer",
]
__requires__ = ["guizero", "Pillow"]

setup(
	name = __project__,
	version = __version__,
	description = __description__,
	packages = __packages__,
	author = __author__,
	author_email = __author_email__,
	classifiers = __classifiers__,
	keywords = __keywords__,
	requires = __requires__,
)
