from setuptools import setup, find_packages

setup (
    name="Youtube Downloader",
    version="0.0.1",
    license="GPL",
    author="blooser",
    url="https://www.github.com/blooser/youtube-downloader",
    author_email="blooser@protonmail.com",
    description="youtube-dl GUI simplify",
    packages=find_packages(),
    package_data = {
        "": ["*.svg", "icons/*.svg"]
    } 
)
