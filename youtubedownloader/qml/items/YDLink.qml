import QtQuick 2.14

import "../util/regex.js" as Regex

YDText {
    id: root

    property string link

    MouseArea {
        id: linkMouseArea

        anchors.fill: parent

        hoverEnabled: true
        enabled: Regex.isUrl(link)
        onClicked: Qt.openUrlExternally(link)
    }

    states: State {
        when: linkMouseArea.containsMouse
        PropertyChanges { target: root; color: Theme.Colors.linkReady }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.hover }
    }
}
