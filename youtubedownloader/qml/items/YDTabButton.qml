import QtQuick 2.14
import QtQuick.Controls 2.14

TabButton {
    id: root

    contentItem: YDText {
        text: root.text
        font: root.font
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
