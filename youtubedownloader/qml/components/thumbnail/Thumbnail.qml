import QtQuick 2.14

import yd.items 0.1

import "../../items" as Items
import "../dynamic" as Dynamic

Items.YDImage {
    id: root

    signal close()

    fillMode: Image.Stretch

    MouseArea {
        anchors.fill: parent
        onClicked: root.close()
    }

    Component {
        id: preDownload

        ThumbnailPreDownload {
            anchors {
                bottom: root.bottom
                bottomMargin: Theme.Margins.tiny
                horizontalCenter: root.horizontalCenter
            }

            visible: (root.status === Image.Ready)
            url: root.source
            dimension: "%1 x %2".arg(root.width).arg(root.height)
        }
    }

}
