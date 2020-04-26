import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items

ItemDelegate {
    id: root

    contentItem: Items.YDText {
        text: root.text
        font: root.font
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 40
        color: Theme.Colors.third
        opacity: root.enabled ? Theme.Visible.on : Theme.Visible.disabled

        Rectangle {
            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }

            width: parent.width
            height: Theme.Size.border

            color: Theme.Colors.second

            visible: !Positioner.isLastItem
        }
    }
}
