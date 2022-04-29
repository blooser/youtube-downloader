import QtQuick 2.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

import youtubedownloader.component.changer


Rectangle {
    id: root

    property string pendingStatus: "waiting"
    property var pendingInfo

    property Component waitingComponent: PendingWaiting {}
    property Component readyComponent: PendingReady {
        pendingInfo: root.pendingInfo
    }

    implicitWidth: changer.implicitWidth
    implicitHeight: Math.max(changer.implicitHeight, 86)

    color: Theme.Colors.second

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        changes: [
            // FIXME: When `when` is prev of component is throws none! Do componentReady method definition

            Change {
                component: waitingComponent
                when: root.pendingStatus === "waiting"
            },

            Change {
                component: readyComponent
                when: root.pendingStatus === "ready"
            }
        ]
    }
}
