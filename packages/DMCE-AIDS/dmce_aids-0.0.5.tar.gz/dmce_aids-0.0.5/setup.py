from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'

DESCRIPTION = 'Python Library for AIDS form DMCE s'
LONG_DESCRIPTION = 'Python Library for AIDS form DMCE'
# Setting up
setup(
    name="DMCE-AIDS",
    version=VERSION,
    author="sdad",
    author_email="aids@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyperclip', 'scikit-learn', 'tensorflow', 'dataset'],
    keywords=['python', 'video', 'stream', 'aids', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'ml = sem6.programs:main'
        ]
    }
)
