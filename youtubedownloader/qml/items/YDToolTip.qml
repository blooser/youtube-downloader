import QtQuick 2.14
import QtQuick.Controls 2.14

ToolTip {
    id: root

    contentItem: YDText {
        text: root.text
        font: text.font
    }

    background: Rectangle {
        color: Theme.Colors.base
        border.color: Theme.Colors.third
    }
}
