import QtQuick 2.14

import "../items" as Items

Rectangle {
    id: root

    property alias text: textItem.text

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
