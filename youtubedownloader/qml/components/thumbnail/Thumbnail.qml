import QtQuick 2.14

import yd.items 0.1

import "../../items" as Items
import "../dynamic" as Dynamic


Items.YDImage {
    id: root

    Component {
        id: preDownload

        ThumbnailPreDownload {
            onClose: console.log("Close")
            onDownload: console.log("Download")
        }
    }

    Dynamic.Changer {
        anchors.fill: parent

        changes: [
            Change {
                component: preDownload
                when: 1 === 1 // TODO: For test, change it
            }
        ]
    }
}
