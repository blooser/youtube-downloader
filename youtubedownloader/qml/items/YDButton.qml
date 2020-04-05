import QtQuick 2.14
import QtQuick.Controls 2.14

Button {
    id: root

    contentItem: YDText {
        text: root.text
        opacity: root.enabled ? 1 : 0
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 40

        opacity: root.enabled ? 1 : 0
        color: root.checked ? Theme.Colors.highlight : Theme.Colors.second

        border {
            color: Theme.Colors.third
            width: root.checked ? Theme.Size.borderBold : Theme.Size.border
        }

        radius: Theme.Margins.tiny
    }
}
