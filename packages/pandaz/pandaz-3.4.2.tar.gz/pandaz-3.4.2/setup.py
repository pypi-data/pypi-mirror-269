from setuptools import setup, find_packages

VERSION = '3.4.2'
DESCRIPTION = 'A package that facilitates efficient coding and development'
LONG_DESCRIPTION = '''
Pandaz is a Python package designed to enhance coding productivity and streamline development workflows. 
It provides utilities and tools that simplify common programming tasks, allowing users to write cleaner, 
more concise code with fewer lines. Pandaz aims to empower developers to focus more on problem-solving 
and less on boilerplate code.
'''

# Setting up
setup(
    name="pandaz",
    version=VERSION,
    author="Tom Hanks",
    author_email="<tomhanks02@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'development', 'productivity', 'utilities'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
