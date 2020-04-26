import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items
import ".." as Components

Components.TileText {
    id: root

    text: downloadOptions.fileFormat

    property var downloadOptions: formatPopup.downloadOptions
    property var link: formatPopup.link

    signal changeFormat(string format)

    FormatPopup {
        id: formatPopup
        anchors.centerIn: parent
        downloadOptions: root.downloadOptions
        link: root.link
        onFormatSelected: root.changeFormat(format)
    }

    MouseArea {
        anchors.fill: parent
        onClicked: formatPopup.open()
    }
}
