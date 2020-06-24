import QtQuick 2.14
import QtQuick.Controls 2.14

ToolButton {
    id: root

    contentItem: YDText {
        text: root.text
        font: root.font
    }

    background: Rectangle {
        implicitWidth: 40
        implicitHeight: 40
        color: root.enabled || root.checked ? Theme.Colors.third : Theme.Colors.base
    }
}
