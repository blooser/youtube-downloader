import QtQuick 2.14
import QtQuick.Controls 2.14

import "../components" as Components

TabButton {
    id: root

    contentItem: Components.IconText {
        text: root.text
        iconSource: root.icon.source
    }

    background: Rectangle {
        id: rectBackground
        color: Theme.Colors.second
    }

    states: State {
        when: root.checked
        PropertyChanges { target: rectBackground; color: Theme.Colors.third }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.quick }
    }
}
