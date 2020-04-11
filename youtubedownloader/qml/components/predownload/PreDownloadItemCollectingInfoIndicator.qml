import QtQuick 2.14

import "../../items" as Items

Rectangle {
    id: root

    implicitHeight: 86

    color: Theme.Colors.second
    radius: Theme.Margins.tiny

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    Items.YDBusyIndicator {
        anchors.centerIn: parent
        running: true
    }
}
