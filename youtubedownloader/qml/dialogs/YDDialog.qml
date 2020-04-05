import QtQuick 2.14
import QtQuick.Controls 2.14

Dialog {
    id: root

    property string dialog: "Unknown"
    property var callback: null

    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose

    anchors.centerIn: Overlay.overlay

    Overlay.modal: Rectangle {
        color: "#99000000"

        Behavior on opacity {
            OpacityAnimator { duration: 250 }
        }
    }

    background: Rectangle {
        implicitWidth: 450
        implicitHeight: 400
        color: Theme.Colors.base
        radius: Theme.Margins.tiny
    }

    enter: Transition {
        NumberAnimation { property: "opacity"; to: 1; duration: 250 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; to: 0; duration: 250 }
    }

    onClosed: dialogManager.close_dialog(dialog)
}
