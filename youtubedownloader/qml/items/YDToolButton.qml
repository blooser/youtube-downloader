import QtQuick 2.14
import QtQuick.Controls 2.14

ToolButton {
    id: root

    contentItem: YDText {
        text: root.text
        font: root.font
        opacity: root.enabled ? Theme.Visible.on : Theme.Visible.disabled
    }

    background: Rectangle {
        implicitWidth: 40
        implicitHeight: 40
        color: root.enabled || root.checked ? Theme.Colors.third : Theme.Colors.base

        Behavior on color {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    }
}
