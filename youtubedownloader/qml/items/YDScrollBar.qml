import QtQuick 2.14
import QtQuick.Controls 2.14

ScrollBar {
    id: root

    size: 0.3
    position: 0.2
    active: true
    orientation: Qt.Vertical

    contentItem: Rectangle {
        implicitWidth: 6
        implicitHeight: 100
        radius: (width/2)
        color: root.pressed ? Theme.Colors.third: Theme.Colors.second

        Behavior on color {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    }
}
