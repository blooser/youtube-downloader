import QtQuick 2.14
import QtQuick.Layouts 1.12


import "../dynamic" as Dynamic

import youtubedownloader.component.changer


import "../../items" as Items
import "../link" as  Link
import ".." as Components

Item {
    id: root

    property string downloadStatus
    property var downloadInfo
    property var downloadOptions
    property var downloadProgress

    signal remove()
    signal resume()
    signal pause()
    signal open()

    implicitWidth: changer.implicitWidth
    implicitHeight: changer.implicitHeight

    property Component downloadingComponent: DownloadItemDownloading {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions
        downloadProgress: root.downloadProgress

        onRemove: root.remove()
        onPause: root.pause()
        onResume: root.resume()
    }

    property Component convertingComponent: DownloadItemConverting {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions
        downloadProgress: root.downloadProgress
    }

    property Component pausedComponent: DownloadItemPaused {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions
        downloadProgress: root.downloadProgress

        onRemove: root.remove()
        onResume: root.resume()
    }

    property Component finishedComponent: DownloadItemFinished {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions

        onRemove: root.remove()
        onOpen: root.open()
    }

    property Component errorComponent: DownloadItemError {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions

        onRemove: root.remove()
    }

    property Component waitingComponent: DownloadItemWaiting {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions
    }

    property Component missingComponent: DownloadItemMissing {
        downloadStatus: root.downloadStatus
        downloadInfo: root.downloadInfo
        downloadOptions: root.downloadOptions

        onRemove: root.remove()
        onResume: root.resume()
    }

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        changes: [
            // FIXME: When `when` is prev of component is throws none! Do componentReady method definition

            Change {
                component: downloadingComponent
                when: root.downloadStatus === "downloading"
            },

            Change {
                component: convertingComponent
                when: root.downloadStatus === "converting"
            },

            Change {
                component: pausedComponent
                when: root.downloadStatus === "paused"
            },

            Change {
                component: finishedComponent
                when: root.downloadStatus === "ready"
            },

            Change {
                component: errorComponent
                when: root.downloadStatus === "error"
            },

            Change {
                component: waitingComponent
                when: root.downloadStatus === "waiting"
            },

            Change {
                component: missingComponent
                when: root.downloadStatus === "missing"
            }
        ]
    }
}
