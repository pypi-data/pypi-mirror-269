from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Pia pia'
LONG_DESCRIPTION = 'A package that pias.'

# Setting up
setup(
    name="piapia",
    version=VERSION,
    author="Yuchi Hsu",
    author_email="yuchihsu0512@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['first package'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
