import QtQuick 2.14
import QtQuick.Controls 2.14

ScrollView {
    id: root

    property color passiveColor: Theme.Colors.second
    property color activeColor: Theme.Colors.third

    YDScrollBar.vertical: YDScrollBar {
        parent: root

        x: root.mirrored ? Theme.Size.none : root.width - width
        y: root.topPadding

        height: root.availableHeight
        active: root.ScrollBar.horizontal.active

        passiveColor: root.passiveColor
        activeColor: root.activeColor
    }

    YDScrollBar.horizontal: YDScrollBar {
        parent: root

        x: root.leftPadding
        y: root.height - height

        width: root.availableWidth
        active: root.ScrollBar.vertical.active

        passiveColor: root.passiveColor
        activeColor: root.activeColor
    }

    background: Rectangle {
        radius: Theme.Margins.tiny

        border {
            width: Theme.Size.border
            color: root.activeFocus ? Theme.Colors.highlight : Theme.Colors.base
        }
    }
}
