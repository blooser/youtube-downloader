import QtQuick 2.14
import QtQuick.Controls 2.14

import "../components" as Components
import "../items" as Items

Dialog {
    id: root

    property string dialog: "Unknown"
    property var callback: null

    property alias headerText: dialogHeader.text

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

    header: Components.DialogHeader {
        id: dialogHeader
    }

    background: Rectangle {
        implicitWidth: 450
        implicitHeight: 400
        color: Theme.Colors.base
        radius: Theme.Margins.tiny
    }

    footer: DialogButtonBox {
        delegate: Items.YDButton {}
        background: null
    }

    enter: Transition {
        NumberAnimation { property: "opacity"; to: 1; duration: 250 }
    }

    exit: Transition {
        NumberAnimation { property: "opacity"; to: 0; duration: 250 }
    }

    onClosed: dialogManager.close_dialog(dialog)
}
