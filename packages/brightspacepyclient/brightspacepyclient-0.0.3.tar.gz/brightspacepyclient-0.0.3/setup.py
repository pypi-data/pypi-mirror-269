from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Python API Client for BrightSpace'

setup(
    name="brightspacepyclient",
    version=VERSION,
    author="CourseCompanion",
    author_email="admin@coursecompanion.ai",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'brightspace'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)