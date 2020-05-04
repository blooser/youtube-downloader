import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property alias error: error.text

    signal remove()

    RowLayout {
        anchors.centerIn: parent
        spacing: Theme.Margins.tiny

        Items.YDImage {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            source: Resources.icons.dizzy
        }

        Items.YDText {
            id: error
            horizontalAlignment: Qt.AlignLeft
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
