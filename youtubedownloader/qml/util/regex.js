const YOUTUBE_LINK_REGEX = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm

function isYoutubeLink(url) {
    let urls = url.match(YOUTUBE_LINK_REGEX)
	
    if (urls === null) {
        return false
	} 

    return urls.length > 0
}

function filterUrlsForYoutubeOnly(urls) {
    var youtubeUrls = []
    for (let url of urls) {
        if (isYoutubeLink(url)) {
            youtubeUrls.push(url)
        }
    }

    return youtubeUrls
}
