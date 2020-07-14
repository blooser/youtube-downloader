import QtQuick 2.14

import "../../items" as Items
import '..' as Components

Item {
    id: root

    property string url
    property string dimension

    signal download(string fileName)

    Row {
        spacing: Theme.Margins.tiny

        anchors {
            horizontalCenter: root.horizontalCenter
            bottom: root.bottom
            bottomMargin: Theme.Margins.big
        }

        ThumbnailFileName {
            id: fileName

            text: Paths.fileName(url)
        }

        Components.ButtonWithBottomText {
            text: qsTr("Download")
            bottomText: root.dimension

            onClicked: root.download(fileName.text)

            enabled: (fileName.text !== "")
        }
    }
}
