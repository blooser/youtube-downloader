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
