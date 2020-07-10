import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../util/regex.js" as Regex


ListView {
    id: root

    property var browser
    property var options

    signal addTab(string url)

    clip: true
    boundsBehavior: Flickable.StopAtBounds
    spacing: Theme.Margins.tiny
    orientation: Qt.Horizontal

    model: browser.tabs

    delegate: BrowserTab {
        Layout.alignment: Qt.AlignLeft
        tabTitle: title
        visible: Regex.isYoutubeLink(url) && !downloadManager.exists(url, root.options)
        onClicked: {
            if (!downloadManager.exists(url, root.options)) {
                root.addTab(url)
            }
        }
    }
}
