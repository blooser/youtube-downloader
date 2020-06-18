import QtQuick 2.14

import "../../items" as Items

Rectangle {
    id: root

    signal close()

    implicitWidth: Theme.Size.icon * 1.5
    implicitHeight: Theme.Size.icon * 1.5

    Items.YDImage {
        source: Resources.icons.close

        anchors.fill: root
    }

    radius: width/2
    color: Theme.Colors.third

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: root.close()
    }
}
