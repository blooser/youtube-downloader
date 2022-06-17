import QtQuick 2.14

import QtQuick.Layouts 1.14


ListView {
    id: root

    boundsBehavior: Flickable.StopAtBounds
    clip: true
    spacing: Theme.Margins.tiny

    remove: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
            NumberAnimation { property: "scale"; from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
        }
    }

    removeDisplaced: Transition {
        PropertyAnimation { property: "y"; duration: Theme.Animation.quick}
    }


}


