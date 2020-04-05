import QtQuick 2.14
import QtQuick.Controls 2.14

ProgressBar {
    id: root

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 4
        color: Theme.Colors.second
        radius: Theme.Margins.tiny
    }

    contentItem: Item {
        implicitWidth: 200
        implicitHeight: 4

        Rectangle {
            width: root.visualPosition * parent.width
            height: parent.height
            color: Theme.Colors.success
            radius: Theme.Margins.tiny
        }
    }
}
