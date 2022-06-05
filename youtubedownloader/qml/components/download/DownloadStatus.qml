import QtQuick 2.14

import ".." as Components
import "../../items" as Items

Flipable {
    id: root

    property var downloadProgress
    property var downloadStatus

    property bool flipped: false

    implicitWidth: front.implicitWidth
    implicitHeight: front.implicitHeight

    onDownloadStatusChanged: {
       // flipped = (downloadStatus === "downloading")
    }

    front: DownloadStatusDetails {
        downloadProgress: root.downloadProgress
        downloadStatus: root.downloadStatus
    }

    back: Item {
        implicitWidth: front.implicitWidth
        implicitHeight: front.implicitHeight

        Components.TileText {
            anchors.centerIn: parent
            text: root.downloadStatus
        }
    }

    transform: Rotation {
        id: rotation

        angle: 0

        origin.x: root.width/2
        origin.y: root.height/2

        axis.x: 1
        axis.z: 0
    }

    state: "front"
    states: [
        State {
            name: "front"
            when: flipped
        },

        State {
            name: "back"
            when: !flipped
            PropertyChanges { target: rotation; angle: 180 }
        }
    ]

    transitions: Transition {
        ParallelAnimation {
            NumberAnimation { properties: "angle"; duration: Theme.Animation.quick }
        }
    }
}
