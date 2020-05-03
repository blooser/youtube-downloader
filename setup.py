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
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt"
    ],
    python_requires=">=3.6"
)
