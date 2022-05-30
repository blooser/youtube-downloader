import QtQuick 2.14

import ".." as Components

Flipable {
    id: root

    property var downloadProgress

    implicitWidth: front.implicitWidth
    implicitHeight: front.implicitHeight


    front: DownloadStatusDetails {
        downloadProgress: root.downloadProgress
    }

    back: DownloadStatusDetails {
        downloadProgress: root.downloadProgress
    }

    transform: Rotation {
        id: rotation

        angle: 0

        origin.x: root.width/2
        origin.y: root.height/2

        axis.x: 1
        axis.z: 0
    }
}
