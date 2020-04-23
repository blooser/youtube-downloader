import QtQuick 2.14

YDText {
    id: root

    property string link

    MouseArea {
        id: linkMouseArea

        anchors.fill: parent

        hoverEnabled: true
        onClicked: Qt.openUrlExternally(link)
    }

    states: State {
        when: linkMouseArea.containsMouse
        PropertyChanges { target: root; color: Theme.Colors.linkReady }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.quick }
    }
}
