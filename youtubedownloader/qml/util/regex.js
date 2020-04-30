const YOUTUBE_LINK_REGEX = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm

function isYoutubeLink(url) {
	let matches = url.match(YOUTUBE_LINK_REGEX)
	
	if (matches === null) {
        return false
	} 

    return matches.length > 0
}
