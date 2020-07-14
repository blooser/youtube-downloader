import QtQuick 2.14

import "../items" as Items

Items.YDButton {
    id: root

    property string bottomText

    Items.YDText {
        anchors {
            bottom: root.bottom
            horizontalCenter: root.horizontalCenter
        }

        opacity: root.enabled ? Theme.Visible.on : Theme.Visible.disabled
        font.pixelSize: Theme.FontSize.groupBoxLabel

        text: root.bottomText
    }
}
