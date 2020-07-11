import QtQuick 2.14
import QtQuick.Controls 2.14

ScrollView {
    id: root

    ScrollBar.vertical: YDScrollBar {
        parent: root

        x: root.mirrored ? 0 : root.width - width
        y: root.topPadding

        height: root.availableHeight
        active: root.ScrollBar.horizontal.active

    }

    background: Rectangle {
        radius: Theme.Margins.tiny

        border {
            width: Theme.Size.border
            color: root.activeFocus ? Theme.Colors.highlight : Theme.Colors.base
        }
    }
}
