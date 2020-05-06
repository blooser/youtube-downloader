import QtQuick 2.14

YDButton {
    id: root

    signal help()

    YDImageButton {
        anchors {
            right: root.right
            rightMargin: Theme.Size.border
            top: root.top
            topMargin: Theme.Size.border
        }

        width: 16
        height: 16

        padding: Theme.Size.borderBold
        imageSource: Resources.icons.question

        onClicked: root.help()

        background: Rectangle {
            radius: Theme.Margins.tiny
            color: Theme.Colors.base
        }
    }
}
