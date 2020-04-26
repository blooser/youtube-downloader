import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items
import ".." as Components

Components.TileText {
    id: root

    property alias downloadOptions: formatPopup.downloadOptions
    property alias link: formatPopup.link

    signal changeFormat(string format)

    FormatPopup {
        id: formatPopup
        anchors.centerIn: parent
        onFormatSelected: root.changeFormat(format)
    }

    MouseArea {
        anchors.fill: parent
        onClicked: formatPopup.open()
    }
}
