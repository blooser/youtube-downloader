import QtQuick 2.14

import "../../items" as Items

Rectangle {
    id: root

    property alias tabTitle: textItem.text

    signal clicked()

    color: Theme.Colors.base
    radius: Theme.Margins.tiny
    border {
        width: Theme.Size.border
        color: Theme.Colors.third
    }

    implicitWidth: textItem.implicitWidth
    implicitHeight: textItem.implicitHeight

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        hoverEnabled: true
    }

    Items.YDTextButton {
        id: textItem

        anchors.centerIn: parent
        padding: Theme.Margins.tiny
        font.pixelSize: Theme.FontSize.micro

        onClicked: root.clicked()
    }

    states: State {
        when: mouseArea.containsMouse
        PropertyChanges { target: root; color: Theme.Colors.third }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.hover }
    }
}
