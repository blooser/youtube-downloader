import QtQuick 2.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

import youtubedownloader.component.changer


Rectangle {
    id: root

    property string status: "waiting"

    property Component waitingComponent: PendingWaiting {}
    property Component readyComponent: PendingReady {}

    implicitWidth: changer.implicitWidth
    implicitHeight: Math.max(changer.implicitHeight, 86)

    color: Theme.Colors.second

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    onStatusChanged: console.log("Status changed: ", status)

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        changes: [
            // FIXME: When `when` is prev of component is throws none! Do componentReady method definition

            Change {
                component: waitingComponent
                when: root.status == "waiting"
            },

            Change {
                component: readyComponent
                when: root.status == "ready"
            }
        ]
    }
}
