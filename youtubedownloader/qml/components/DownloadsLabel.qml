import QtQuick 2.14

import "../items" as Items

Rectangle {
    id: root

    property alias text: textItem.text
    property alias counter: counter.text

    radius: Theme.Margins.tiny
    color: Theme.Colors.third

    implicitWidth: textItem.implicitWidth
    implicitHeight: textItem.implicitHeight

    Items.YDText {
        id: textItem
        anchors.centerIn: parent
        padding: Theme.Margins.tiny

        TileText {
            id: counter

            width: height // NOTE: Smooth circle

            anchors {
                left: parent.right
                top: parent.top
                topMargin: Theme.Size.borderBold
            }

            radius: width/2
            font.pixelSize: Theme.FontSize.micro
            style: Text.Raised
            styleColor: Theme.Colors.textStyle
            padding: Theme.Size.borderBold
            color: Theme.Colors.second
        }
    }
}
