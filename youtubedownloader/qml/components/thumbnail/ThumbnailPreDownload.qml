import QtQuick 2.14

import "../../items" as Items

Item {
    id: root

    property string url

    signal download(string fileName)

    Column {
        spacing: Theme.Margins.tiny

        anchors {
            horizontalCenter: root.horizontalCenter
            bottom: root.bottom
            bottomMargin: Theme.Margins.big
        }

        ThumbnailFileName {
            id: fileName

            anchors.horizontalCenter: parent.horizontalCenter

            text: Paths.fileName(url)
        }

        Items.YDButton {
            text: qsTr("Download")

            anchors.horizontalCenter: parent.horizontalCenter

            onClicked: root.download(fileName.text)

            enabled: (fileName.text !== "")
        }
    }
}
