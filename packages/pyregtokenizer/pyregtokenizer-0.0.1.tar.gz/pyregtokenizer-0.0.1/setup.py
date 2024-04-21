from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A BPE Tokenizer using regex'

# Setting up
setup(
    name="pyregtokenizer",
    version=VERSION,
    author="Echo.ai (Pratyaksh Agarwal)",
    author_email="pratyakshagarwal93@gmail.com",
    description=DESCRIPTION, # Using the same description as long description
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['regex'],
    keywords=['python', 'bpe', 'tokenizer', 'regex'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
