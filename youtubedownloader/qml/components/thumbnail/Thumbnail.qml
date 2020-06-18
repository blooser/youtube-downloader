import QtQuick 2.14

import yd.items 0.1

import "../../items" as Items
import "../dynamic" as Dynamic


Items.YDImage {
    id: root

    signal close()

    Component {
        id: preDownload

        ThumbnailPreDownload {
            onClose: root.close()
            onDownload: console.log("Download")
        }
    }

    Dynamic.Changer {
        anchors.fill: parent

        changes: [
            Change {
                component: preDownload
                when: (FileDownloader.currentDownload === undefined)
            }
        ]
    }}
