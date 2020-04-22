import QtQuick 2.14

import "../../items" as Items

Rectangle {
    id: root

    radius: Theme.Margins.tiny
    color: Theme.Colors.shadowError

    Items.YDText {
        id: textItem

        anchors.centerIn: parent
        text: qsTr("Already exists")
    }
}
