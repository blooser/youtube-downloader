import QtQuick 2.14
import QtQuick.Controls 2.14

import "../components" as Components

ToolBar {
    id: root

    background: Rectangle {
        implicitHeight: 40
        color: Theme.Colors.second

        Rectangle {
            width: parent.width
            height: Theme.Size.border
            anchors.bottom: parent.bottom
            color: Theme.Colors.third
        }
    }
}
