import QtQuick 2.14
import QtGraphicalEffects 1.14

import "../../items" as Items

Item {
    id: root

    signal remove()

    Items.YDBusyIndicator {
        anchors.centerIn: parent
        running: true

        Items.YDImage {
            id: youtubeIcon
            anchors.centerIn: parent
            source: Resources.logo
            width: 32
            height: 32
        }
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
