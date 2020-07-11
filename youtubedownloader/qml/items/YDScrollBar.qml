import QtQuick 2.14
import QtQuick.Controls 2.14

ScrollBar {
    id: root

    size: 0.3
    position: 0.2
    active: true
    orientation: Qt.Vertical

    property color passiveColor: Theme.Colors.second
    property color activeColor: Theme.Colors.third

    contentItem: Rectangle {
        implicitWidth: root.orientation === Qt.Vertical ?  6 : 100
        implicitHeight: root.orientation === Qt.Vertical ? 100 : 6
        radius: (width/2)
        opacity: root.hovered || root.active
        color: root.pressed ? activeColor : passiveColor

        Behavior on color {
            ColorAnimation { duration: Theme.Animation.quick }
        }

        Behavior on opacity {
            NumberAnimation { duration: Theme.Animation.quick }
        }
    }
}
