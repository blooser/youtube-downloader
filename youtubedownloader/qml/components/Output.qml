import QtQuick 2.15

import "../items" as Items
import ".." as Components

Rectangle {
    id: root

    property var itemOptions
    property var itemInfo

    implicitWidth: output.implicitWidth
    implicitHeight: output.implicitHeight

    color: Theme.Colors.base
    radius: 5

    Items.YDText {
        id: output

        font.pixelSize: Theme.FontSize.micro

        padding: Theme.Size.borderBold

        text: qsTr("%1/%2.%3").arg(root.itemOptions.output)
                              .arg(root.itemInfo.filename)
                              .arg(root.itemOptions.format)
    }
}
