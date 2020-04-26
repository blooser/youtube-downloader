import QtQuick 2.14
import QtQuick.Controls 2.14

Popup {

    modal: true
    focus: true

    Overlay.modal: Rectangle {
        color: Theme.Colors.shadowBlack

        Behavior on opacity {
            NumberAnimation { property: "opacity"; duration: Theme.Animation.quick }
        }
    }

    background: Rectangle {
        border.color: Theme.Colors.third
        color: Theme.Colors.base
        radius: Theme.Margins.tiny
    }

    enter: Transition {
        NumberAnimation { property: "opacity"; to: Theme.Visible.on; duration: Theme.Animation.quick }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; to: Theme.Visible.off; duration: Theme.Animation.quick }
    }
}
