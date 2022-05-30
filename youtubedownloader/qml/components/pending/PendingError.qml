import QtQuick 2.15

import "../../items" as Items
import "../buttons" as Buttons

Rectangle {
    id: root

    property var pendingInfo

    signal remove()

    color: Theme.Colors.error

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    Items.YDText {
        anchors.centerIn: root

        text: pendingInfo.error
    }

    Buttons.DeleteButton {
        anchors {
            right: parent.right
            rightMargin: Theme.Margins.normal
            verticalCenter: parent.verticalCenter
        }

        onRemove: root.remove()
    }
}
