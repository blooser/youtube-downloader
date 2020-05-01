import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items


PreDownloadItemInfo {
    id: root

    Items.YDText {
        anchors {
            top: root.top
            horizontalCenter: root.horizontalCenter
        }

        font {
            bold: true
            pixelSize: Theme.FontSize.tiny
        }

        text: qsTr("Destination file exists")
    }
}

