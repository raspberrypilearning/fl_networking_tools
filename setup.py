from setuptools import setup

__project__ = "fl_networking_tools"
__version__ = "0.0.6"
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
__requires__ = ["pillow"]
__python_requires__ = ">=3"

__long_description__ = """# FL Networking tools

This module and it's contents are intended for use on the FutureLearn course - Networking with Python: Socket programming for communication(LINKWHENLIVE)

## Text messaging

The functions `send_text()` and `get_text()` can be used to send any text messages using a terminator character. 

It is used in week 1 of the course. 

## Image viewer

The image viewer class can be used to display any image in a UI created with the tkinter library.   

It is used in week 2 of the course, to send an image over UDP. 

## Binary messaging

The functions `send_binary()` and `get_binary()` are used to send binary data, these functions use headers to set a message length. 

They are used in week 3 of the course, to send and receive the data neccessary for the quiz."""



setup(
	name = __project__,
	version = __version__,
	description = __description__,
	packages = __packages__,
	author = __author__,
	author_email = __author_email__,
	classifiers = __classifiers__,
	keywords = __keywords__,
	install_requires = __requires__,
	python_requires = __python_requires__,
	long_description = __long_description__,
)
