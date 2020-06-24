const WINDOW_MARGIN = 175

function progress(value, to) {
    let number = Math.floor((value/to) * 100)

    if (isNaN(number)) {
        return ""
    }

    let msg = (number === 100 ? String("%1% finished") : String("%1%")).arg(number)
    return msg
}
