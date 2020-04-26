import QtQuick 2.14
import QtQuick.Layouts 1.12

import yd.items 0.1

import "../../items" as Items
import "../link" as Link
import ".." as Components
import "../dynamic" as Dynamic

Rectangle {
    id: root

    property string destinationFile
    property string preDownloadStatus
    property string thumbnailUrl
    property string link
    property string linkTitle
    property string linkUploader
    property string linkUploaderLink
    property string linkDuration

    property var downloadOptions

    signal remove()
    signal changeFormat(string format)

    implicitWidth: changer.implicitWidth
    implicitHeight: Math.max(changer.implicitHeight, 86)

    color: Theme.Colors.second
    radius: Theme.Margins.tiny

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    Component {
        id: collectingInfoIndicator
        PreDownloadItemCollectingInfoIndicator {}
    }

    Component {
        id: itemInfo
        PreDownloadItemInfo {
            thumbnailUrl: root.thumbnailUrl
            link: root.link
            linkTitle: root.linkTitle
            linkUploader: root.linkUploader
            linkUploaderLink: root.linkUploaderLink
            linkDuration: root.linkDuration
            downloadOptions: root.downloadOptions
            onRemove: root.remove()
            onChangeFormat: root.changeFormat(format)
        }
    }

    Component {
        id: alreadyExistsIndicator
        PreDownloadItemAlreadyExistsIndicator {
            existsPath: root.destinationFile
            PreDownloadItemInfo {
                anchors.fill: parent
                opacity: Theme.Visible.disabled
                thumbnailUrl: root.thumbnailUrl
                linkTitle: root.linkTitle
                linkUploader: root.linkUploader
                linkDuration: root.linkDuration
                downloadOptions: root.downloadOptions
                onRemove: root.remove()
            }
        }
    }

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        changes: [
            Change {
                component: collectingInfoIndicator
                when: (preDownloadStatus === "processing")
            },

            Change {
                component: itemInfo
                when: (preDownloadStatus === "ready")

            },

            Change {
                component: alreadyExistsIndicator
                when: (preDownloadStatus === "exists")
            }
        ]
    }
}
