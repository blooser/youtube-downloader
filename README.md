


<div align="center">
	<img src="https://raw.githubusercontent.com/blooser/youtube-downloader/08c713ea717a2a723d06ef4faeb19f9bbdf04784/youtubedownloader/resources/youtube-downloader-with-text.svg" width="350" height="350">
</div>

Youtube downloader is a [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) helper for [youtube-dl](https://github.com/ytdl-org/youtube-dl/). It provides a graphical interface to download videos from YouTube.com and other sites with conveniences like track the download, pause, or select the media format.

## Project status

The project has been reincarnated. I rebuild the backend and starting to continue with the work, all features will be implemented making the software more comfortable to the usage.

## Usage

The youtube-downloader provides a friendly graphical interface for downloading media resources from the remote clients.

![preview](https://i.postimg.cc/GhpsTpLT/Zrzut-ekranu-Deepin-plasmashell-20220629190129.png)

## Dependency

This software is based on [PySide6](https://www.qt.io/qt-for-python) and [youtube-dl](https://github.com/ytdl-org/youtube-dl/).

## History

The program stores all downloaded items in the database, in every time you can just download again item from the history's context.

![history](https://i.postimg.cc/4x77wFhJ/Zrzut-ekranu-Deepin-plasmashell-20220629190155.png)

## Web Browser integration

Youtube Downloader is integrated with Firefox, that's mean it will read currently opened tabs with YouTube's links. It provides a feature to quick download currently played videos from YouTube.

## Supported browsers

It is easy to check if your URL is valid.

![browsers](https://i.postimg.cc/tCmn3HJS/Zrzut-ekranu-Deepin-plasmashell-20220629190210.png)

## Installation

Prepare youtube downloader to work.

### Manual

```bash
git clone https://github.com/blooser/youtube-downloader && cd youtube-downloader
python setup.py build
sudo setup.py install 
```

### PyPi

```bash
pip install youtube-downloader
```

## License

Youtube downloader is a free software released under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).



