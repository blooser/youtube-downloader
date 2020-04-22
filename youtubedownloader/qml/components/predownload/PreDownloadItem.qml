import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as Link
import ".." as Components

Rectangle {
    id: root

    property string preDownloadStatus
    property string thumbnailUrl
    property string linkTitle
    property string linkUploader
    property string linkDuration
    property string selectedFormat

    signal remove()

    implicitWidth: loader.implicitWidth
    implicitHeight: Math.max(loader.implicitHeight, 86)

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
            linkTitle: root.linkTitle
            linkUploader: root.linkUploader
            linkDuration: root.linkDuration
            selectedFormat: root.selectedFormat
            onRemove: root.remove()
        }
    }

    Component {
        id: alreadyExistsIndicator
        PreDownloadItemAlreadyExistsIndicator {
            PreDownloadItemInfo {
                anchors.fill: parent
                opacity: Theme.Visible.disabled
                thumbnailUrl: root.thumbnailUrl
                linkTitle: root.linkTitle
                linkUploader: root.linkUploader
                linkDuration: root.linkDuration
                selectedFormat: root.selectedFormat
                onRemove: root.remove()
            }
        }
    }

    Loader {
        id: loader

        anchors.fill: parent
    }

    state: "processing"
    states: [
        State {
            name: "processing"
            when: (preDownloadStatus === "processing")
            PropertyChanges { target: loader; sourceComponent: collectingInfoIndicator }
        },

        State {
            name: "ready"
            when: (preDownloadStatus === "ready")
            PropertyChanges { target: loader; sourceComponent: itemInfo }
        },

        State {
            name: "exists"
            when: (preDownloadStatus === "exists")
            PropertyChanges { target: loader; sourceComponent: alreadyExistsIndicator }
        }
    ]
}
