const URL_REGEX = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/
const YOUTUBE_LINK_REGEX = /http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/gm

function isUrl(url){
    let matches = url.match(URL_REGEX)
    return (matches !== null && matches.length > 0)
}

function extractUrls(text) {
    let lines = text.split("\n")
    var urls = []

    for (const line of lines) {
        if (isUrl(line)) {
            urls.push(line)
        }
    }

    return urls
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
