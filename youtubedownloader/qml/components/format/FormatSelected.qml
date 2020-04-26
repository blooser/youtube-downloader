import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items
import ".." as Components

Components.TileText {
    id: root

    FormatPopup {
        id: formatPopup
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: formatPopup.open()
    }
}
