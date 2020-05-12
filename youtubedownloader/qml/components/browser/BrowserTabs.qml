import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../util/regex.js" as Regex

Flickable {
    id: root

    implicitHeight: mainLayout.implicitHeight

    contentWidth: mainLayout.implicitWidth

    clip: true
    boundsBehavior: Flickable.StopAtBounds

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Repeater {
            model: Firefox.tabs

            BrowserTab {
                Layout.alignment: Qt.AlignLeft
                tabTitle: modelData.title
                visible: Regex.isYoutubeLink(modelData.url)
            }
        }
    }
}
