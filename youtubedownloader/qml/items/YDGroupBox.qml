import QtQuick 2.14
import QtQuick.Controls 2.14

GroupBox {
    id: root

    background: Rectangle {
        y: root.topPadding - root.bottomPadding
        width: parent.width
        height: parent.height - root.topPadding + root.bottomPadding
        color: Theme.Colors.blank
        border.color: Theme.Colors.third
        radius: Theme.Margins.tiny
    }
}
