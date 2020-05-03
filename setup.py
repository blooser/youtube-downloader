from setuptools import setup

setup (
    name="Youtube Downloader",
    version="0.0.1",
    license="GPL",
    author="blooser",
    url="https://www.github.com/blooser/youtube-downloader",
    author_email="blooser@protonmail.com",
    description="youtube-dl GUI simplify",
    packages=[
        "youtubedownloader", "youtubedownloader.resources"
    ],

    package_data = {
        "": ["*.svg", "icons/*.svg", "qml/*.qml", "qml/*/*", "qml/*/*/*"]
    },
    data_files = [
        ("/usr/share/applications", ["doc/yd.desktop"]),
        ("/usr/share/icons", ["youtubedownloader/resources/yd.svg"])
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt"
    ],
    entry_points = {
        "console_scripts": ["youtubedownloader = youtubedownloader:main"]
    },
    python_requires=">=3.6"
)
