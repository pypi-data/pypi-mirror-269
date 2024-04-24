from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'The only method package you will need.'
LONG_DESCRIPTION = 'Inside of this package, you will find any single method to go against anybody that insults you.'

# Setting up
setup(
        name="the_methods_you_need", 
        version=VERSION,
        author="Batu Engin",
        author_email="batueng@umich.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)