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
            onDownload: dialogManager.open_dialog("SelectDirectoryDialog", {}, function (url) {
                fileDownloader.download(root.source, String("%1/%2").arg(Paths.cleanPath(url)).arg(fileName))
            })
        }
    }

    Component {
        id: download

        ThumbnailDownload {
            anchors {
                bottom: root.bottom
                bottomMargin: Theme.Margins.tiny
                left: root.left
                leftMargin: Theme.Margins.big
                right: root.right
                rightMargin: Theme.Margins.big
            }

            visible: (root.status === Image.Ready)
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
