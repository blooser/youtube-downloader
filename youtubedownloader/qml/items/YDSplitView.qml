import QtQuick 2.14
import QtQuick.Controls 2.14

SplitView {
    id: root

    handle: Rectangle {
        implicitWidth: Theme.Margins.tiny
        implicitHeight: Theme.Margins.tiny
        color: SplitHandle.pressed ? Theme.Colors.highlight
                                   : (SplitHandle.hovered) ? Theme.Colors.third : Theme.Colors.second

        Behavior on color {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    }
}
