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
    property string link

    property var downloadData
    property var downloadOptions

    signal remove()
    signal changeFormat(string format)
    signal changeOutputPath(string path)

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
        PreDownloadItemCollectingInfoIndicator {
            onRemove: root.remove()
        }
    }

    Component {
        id: itemError
        PreDownloadItemError {
            error: root.preDownloadStatus
            onRemove: root.remove()
        }
    }

    Component {
        id: itemInfo
        PreDownloadItemInfo {
            link: root.link
            downloadData: root.downloadData
            downloadOptions: root.downloadOptions
            onRemove: root.remove()
            onChangeFormat: root.changeFormat(format)
            onChangeOutputPath: root.changeOutputPath(path)
        }
    }

    Component {
        id: alreadyExistsIndicator
        PreDownloadItemAlreadyExistsIndicator {
            link: root.link
            downloadData: root.downloadData
            downloadOptions: root.downloadOptions
            onRemove: root.remove()
            onChangeFormat: root.changeFormat(format)
            onChangeOutputPath: root.changeOutputPath(path)
        }
    }

    states: State {
        when: (preDownloadStatus === "exists" || preDownloadStatus.includes("unsupported") || preDownloadStatus.includes("ERROR"))
        PropertyChanges { target: root; color: Theme.Colors.shadowError }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.quick }
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
            },


            Change {
                component: itemError
                when: (preDownloadStatus.includes("ERROR") || preDownloadStatus.includes("unsupported"))
            }
        ]
    }
}
