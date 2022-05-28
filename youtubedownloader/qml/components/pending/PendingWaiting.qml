import QtQuick 2.15

import "../../items" as Items
import "../buttons" as Buttons

Rectangle {
    id: root

    signal remove()

    color: Theme.Colors.second

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    Items.YDBusyIndicator {
        anchors.centerIn: parent
        running: true
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
