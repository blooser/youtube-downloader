import QtQuick 2.14

import "../../items" as Items

Rectangle {
    id: root

    property alias tabTitle: textItem.text

    signal clicked()

    color: Theme.Colors.blank
    radius: Theme.Margins.tiny
    border {
        width: Theme.Size.border
        color: Theme.Colors.third
    }

    implicitWidth: textItem.implicitWidth
    implicitHeight: textItem.implicitHeight

    Items.YDTextButton {
        id: textItem

        anchors.centerIn: parent
        padding: Theme.Margins.tiny
        font.pixelSize: Theme.FontSize.micro

        onClicked: root.clicked()
    }
}
