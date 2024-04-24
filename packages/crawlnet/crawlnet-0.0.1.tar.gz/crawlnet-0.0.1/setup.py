from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'CrawlNet'
 
# Setting up
setup(
    name="crawlnet",
    version=VERSION,
    author="Hrushikesh Kachgunde",
    author_email="<hrushiskachgunde@gmail.com>",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', "deap", "pandas"],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)