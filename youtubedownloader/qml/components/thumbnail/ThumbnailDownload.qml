import QtQuick 2.14
import "../dynamic" as Dynamic


import youtubedownloader.component.changer

Item {
    id: root

    implicitWidth: changer.implicitWidth
    implicitHeight: changer.implicitHeight

    property Component downloadButtonComponent: ThumbnailDownloadButton {
        onDownload: (path) => {
            console.log("Downloading ", path)
        }
    }

    property Component downloadingComponent: ThumbnailDownloading {

    }

    Dynamic.Changer {
        id: changer

        changes: [
            Change {
                component: downloadButtonComponent
                when: true
            },

            Change {
                component: downloadingComponent
                when: false
            }
        ]
    }
}
