from setuptools import setup, find_packages

VERSION = '1.1.2'
DESCRIPTION = 'Helps users code efficently'
LONG_DESCRIPTION = 'A package that allows to build simple codes in a well defined and efficient manner.'

# Setting up
setup(
    name="pandaz",
    version=VERSION,
    author="Tom Hanks",
    author_email="<tomhanks02@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)


