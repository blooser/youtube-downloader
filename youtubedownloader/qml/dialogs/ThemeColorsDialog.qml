import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

import "../components/themecolors" as ThemeColors


YDDialog {
    id: root

    dialog: "ThemeColorsDialog"

    anchors.centerIn: undefined

    implicitHeight: 225

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    header: null
    footer: null
    background: null
    standardButtons: Dialog.NoButton

    contentItem: ThemeColors.ThemeColors {}

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "y"; from: root.y; to: root.y - root.implicitHeight; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; from: Theme.Visible.off; to: Theme.Visible.on; duration: Theme.Animation.quick }
        }
    }

    exit: Transition {
        ParallelAnimation {
            NumberAnimation { property: "y"; from: root.y; to: root.y + root.implicitHeight; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
        }
    }

    Connections {
        target: Theme

        function onColorsChanged(colors) {
            Settings.themeColor = colors.base
        }
    }
}
