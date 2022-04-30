import QtQuick 2.14

import QtQuick.Layouts 1.14


ListView {
    boundsBehavior: Flickable.StopAtBounds
    clip: true
    spacing: Theme.Margins.tiny

    add: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; to: Theme.Visible.on; duration: Theme.Animation.quick }
            NumberAnimation { property: "scale"; to: Theme.Visible.on; duration: Theme.Animation.quick }
        }
    }

    removeDisplaced: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; to: Theme.Visible.off; duration: Theme.Animation.quick }
            NumberAnimation { property: "scale"; to: Theme.Visible.off; duration: Theme.Animation.quick }
        }
    }
}


