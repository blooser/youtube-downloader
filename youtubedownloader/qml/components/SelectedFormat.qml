import QtQuick 2.14

import "../items" as Items

Rectangle {
    id: root

    property alias format: format.text

    implicitWidth: 50
    implicitHeight: 50

    color: Theme.Colors.third
    radius: Theme.Margins.tiny

    border {
        color: Theme.Colors.base
        width: Theme.Size.border
    }

    Items.YDText {
        id: format

        anchors.centerIn: parent
    }
}
