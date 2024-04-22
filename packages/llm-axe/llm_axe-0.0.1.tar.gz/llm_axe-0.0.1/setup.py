from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A toolkit for quicky implementing complex interactions for local LLMs'
LONG_DESCRIPTION = 'A toolkit for quicky implementing complex interactions for local LLMs. Includes features such as function callers, online agents, pre-made generic agents, and more.'

# Setting up
setup(
        name="llm_axe", 
        version=VERSION,
        author="Emir Sahin",
        author_email="emirsah122@gmail.com",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        
        keywords=['python', 'llm axe', 'llm toolkit', 'local llm', 'local llm internet', 'function caller llm'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)