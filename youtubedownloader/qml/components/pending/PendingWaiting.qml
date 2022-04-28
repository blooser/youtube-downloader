import QtQuick 2.15

import "../../items" as Items

Item {
    id: root

    signal remove()

    Items.YDBusyIndicator {
        anchors.centerIn: parent
        running: true
    }

    Items.YDImageButton {
        anchors {
            right: parent.right
            rightMargin: Theme.Margins.normal
            verticalCenter: parent.verticalCenter
        }

        width: Theme.Size.icon
        height: Theme.Size.icon

        imageSource: Resources.icons.delete

        onClicked: root.remove()
    }
}
