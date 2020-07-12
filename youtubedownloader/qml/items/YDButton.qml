import QtQuick 2.14
import QtQuick.Controls 2.14

import "../components" as Components

Button {
    id: root

    contentItem: Components.IconText {
        opacity: root.enabled ? Theme.Visible.on : Theme.Visible.disabled
        iconSource: icon.source
        text: root.text
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 40

        opacity: root.enabled ? Theme.Visible.on : Theme.Visible.disabled
        color: root.checked ? Theme.Colors.highlight : Theme.Colors.second

        border {
            color: Theme.Colors.third
            width: root.checked ? Theme.Size.borderBold : Theme.Size.border
        }

        radius: Theme.Margins.tiny

        Behavior on color {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    }
}
