import QtQuick 2.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

import youtubedownloader.component.changer


Item {
    id: root

    property string pendingStatus: "waiting"
    property var pendingInfo
    property var pendingOptions

    signal formatSelected(string format)
    signal changeOutput(string path)
    signal remove()
    signal forceRemove()

    property Component waitingComponent: PendingWaiting {
        onRemove: root.forceRemove()
    }
    property Component errorComponent: PendingError {
        pendingInfo: root.pendingInfo

        onRemove: root.forceRemove()
    }
    property Component readyComponent: PendingReady {
        pendingInfo: root.pendingInfo
        pendingOptions: root.pendingOptions

        onFormatSelected: format => { root.formatSelected(format) }
        onRemove: root.remove()
        onChangeOutput: path => { root.changeOutput(path) }
    }

    implicitWidth: changer.implicitWidth
    implicitHeight: Math.max(changer.implicitHeight, 86)

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
            },

            Change {
                component: errorComponent
                when: root.pendingStatus === "error"
            }
        ]
    }
}
