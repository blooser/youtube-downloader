import QtQuick 2.14

import yd.items 0.1

import "../../items" as Items
import "../dynamic" as Dynamic

Items.YDImage {
    id: root

    signal close()

    ThumbnailCloseButton {
        anchors {
            right: root.right
            rightMargin: -(width/2)
            top: root.top
            topMargin: -(height/2)
        }

        onClose: root.close()
    }

    Component {
        id: preDownload

        ThumbnailPreDownload {
            onDownload: dialogManager.open_dialog("SelectDirectoryDialog", {}, function (url) {
                FileDownloader.download(root.source, Paths.cleanPath(url))
            })
        }
    }

    Component {
        id: download

        ThumbnailDownload {
            to: FileDownloader.currentDownload.progress.totalBytes
            value: FileDownloader.currentDownload.progress.readBytes
            outputUrl: FileDownloader.currentDownload.outputUrl
        }
    }

    Dynamic.Changer {
        anchors.fill: parent

        changes: [
            Change {
                component: preDownload
                when: (FileDownloader.currentDownload === undefined)
            },

            Change {
                component: download
                when: (FileDownloader.currentDownload !== undefined)
            }
        ]
    }

    Component.onDestruction: {
        if (FileDownloader.currentDownload !== undefined) {
            FileDownloader.clear()
        }
    }
}
