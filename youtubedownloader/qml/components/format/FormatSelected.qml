import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items
import ".." as Components

Components.TileText {
    id: root

    property var options: formatPopup.downloadOptions

    signal formatSelected(string format)

    text: options.format

    FormatPopup {
        id: formatPopup

        anchors.centerIn: parent

        options: root.options

        onFormatSelected: format => { root.formatSelected(format) }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: formatPopup.open()
    }
}
