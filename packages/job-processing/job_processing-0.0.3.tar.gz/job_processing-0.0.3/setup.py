from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Job Processing Package'
LONG_DESCRIPTION = 'Package for processing jobs in a batch system'

# Setting up
setup(
    name="job_processing",
    version=VERSION,
    author="Dominik Sebesic",
    author_email="<sebesic.dominik@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'job processing'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
