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
            url: root.source
            dimension: "%1 x %2".arg(root.width).arg(root.height)
            onDownload: dialogManager.open_dialog("SelectDirectoryDialog", {}, function (url) {
                fileDownloader.download(root.source, String("%1/%2").arg(Paths.cleanPath(url)).arg(fileName))
            })
        }
    }

    Component {
        id: download

        ThumbnailDownload {
            to: fileDownloader.currentDownload.progress.totalBytes
            value: fileDownloader.currentDownload.progress.readBytes
            outputUrl: fileDownloader.currentDownload.outputUrl
        }
    }

    Dynamic.Changer {
        anchors.fill: parent

        changes: [
            Change {
                component: preDownload
                when: (fileDownloader.currentDownload === undefined)
            },

            Change {
                component: download
                when: (fileDownloader.currentDownload !== undefined)
            }
        ]
    }

    Component.onDestruction: {
        if (fileDownloader.currentDownload !== undefined) {
            fileDownloader.clear()
        }
    }
}
