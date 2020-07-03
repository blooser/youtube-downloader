import QtQuick 2.14

import "../../items" as Items

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

        Items.YDButton {
            text: qsTr("Download")

            onClicked: root.download(fileName.text)

            enabled: (fileName.text !== "")

            Items.YDText {
                anchors {
                    bottom: parent.bottom
                    horizontalCenter: parent.horizontalCenter
                }

                font.pixelSize: Theme.FontSize.groupBoxLabel
                text: root.dimension
            }
        }
    }
}
