const URL_REGEX = /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/
const YOUTUBE_LINK_REGEX = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm

function isUrl(url){
    let matches = url.match(URL_REGEX)
    return (matches !== null && matches.length > 0)
}

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
