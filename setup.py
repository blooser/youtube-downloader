from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup (
    name="youtube-downloader",
    version="0.3.2",
    license="GPLv3",
    author="blooser",
    url="https://www.github.com/blooser/youtube-downloader",
    author_email="blooser@protonmail.com",
    description="youtube-dl GUI simplify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "youtubedownloader", "youtubedownloader.resources"
    ],
    package_data = {
        "": ["*.svg", "icons/*.svg", "qml/*.qml", "qml/*/*", "qml/*/*/*"]
    },
    data_files = [
        ("/usr/local/share/applications", ["doc/youtube-downloader.desktop"]),
        ("/usr/local/share/icons/hicolor/scalable/apps", ["youtubedownloader/resources/youtube-downloader.svg"])
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt"
    ],
    entry_points = {
        "console_scripts": ["youtube-downloader = youtubedownloader:main"]
    },
    install_requires = [
        "PySide2",
        "lz4",
        "youtube-dl"
    ],
    keywords = "qt qml pyside2 youtube download youtube-dl",
    python_requires=">=3.6"
)
