import QtQuick 2.14

import "../items" as Items

Rectangle {
    id: root

    property alias text: textItem.text
    property alias font: textItem.font
    property alias padding: textItem.padding
    property alias style: textItem.style
    property alias styleColor: textItem.styleColor

    radius: Theme.Margins.tiny
    color: Theme.Colors.third

    implicitWidth: textItem.implicitWidth
    implicitHeight: textItem.implicitHeight

    Items.YDText {
        id: textItem
        anchors.centerIn: parent
        padding: Theme.Margins.tiny
    }
}
