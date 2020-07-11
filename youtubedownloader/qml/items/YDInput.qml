import QtQuick 2.14
import QtQuick.Controls 2.14

TextField {
    id: root

    color: Theme.Colors.text

    property bool icon: false
    property url iconSource

    signal iconClicked()

    rightPadding: root.icon ? Theme.Margins.big * 2 : Theme.Margins.tiny

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 40

        radius: Theme.Margins.tiny
        color: Theme.Colors.second
        border {
            width: Theme.Size.border
            color: root.activeFocus ? Theme.Colors.highlight : Theme.Colors.base
        }

        Behavior on border.color {
            ColorAnimation { duration: Theme.Animation.quick }
        }

        YDPureImageButton {
            implicitWidth: 16
            implicitHeight: 16

            visible: root.icon
            imageSource: root.iconSource

            anchors {
                right: parent.right
                rightMargin: Theme.Margins.small
                verticalCenter: parent.verticalCenter
            }

            onClicked: root.iconClicked()
        }
    }
}
