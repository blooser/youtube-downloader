import QtQuick 2.14

import ".." as Components

Flipable {
    id: root

    property bool flipped: false

    property string status

    implicitWidth: frontText.implicitWidth
    implicitHeight: frontText.implicitHeight

    onStatusChanged: {
        if (flipped) {
            frontText.text = status
        } else {
            backText.text = status
        }

        flipped = !flipped
    }

    front: Components.TileText {
        id: frontText
    }

    back: Components.TileText {
        id: backText
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
            PropertyChanges { target: rotation; angle: 180 }
            PropertyChanges { target: root; implicitWidth: backText.implicitWidth; implicitHeight: backText.implicitHeight }
        },

        State {
            name: "back"
            when: !flipped
            PropertyChanges { target: root; implicitWidth: frontText.implicitWidth; implicitHeight: frontText.implicitHeight }
        }
    ]

    transitions: Transition {
        ParallelAnimation {
            NumberAnimation { properties: "angle"; duration: Theme.Animation.quick }
            NumberAnimation { properties: "implicitWidth, implicitHeight"; duration: Theme.Animation.quick }
        }
    }
}
