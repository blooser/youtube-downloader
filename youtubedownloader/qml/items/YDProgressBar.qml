import QtQuick 2.14
import QtQuick.Controls 2.14

ProgressBar {
    id: root

    property bool error: false
    property double radius: Theme.Margins.tiny

    background: Rectangle {
        id: backgroundRect

        implicitWidth: 200
        implicitHeight: 4
        color: root.indeterminate ? Theme.Colors.processing :
                       root.error ? Theme.Colors.error : Theme.Colors.second
        radius: root.radius
    }

    contentItem: Item {
        implicitWidth: 200
        implicitHeight: 4

        Rectangle {
            width: root.visualPosition * parent.width
            height: parent.height
            color: Theme.Colors.success
            radius: root.radius
            visible: !root.error
        }
    }

    Behavior on value {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
