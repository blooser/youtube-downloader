import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../util/regex.js" as Regex

Flickable {
    id: root

    property var browser
    property var options

    signal addTab(string url)

    implicitHeight: mainLayout.implicitHeight

    contentWidth: mainLayout.implicitWidth

    clip: true
    boundsBehavior: Flickable.StopAtBounds

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Repeater {
            model: browser.tabs

            BrowserTab {
                Layout.alignment: Qt.AlignLeft
                tabTitle: modelData.title
                visible: Regex.isYoutubeLink(modelData.url) && !downloadManager.exists(modelData.url, root.options)
                onClicked: {
                    if (!downloadManager.exists(modelData.url, root.options)) {
                        root.addTab(modelData.url)
                    }
                }
            }
        }
    }

    Behavior on implicitHeight {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
