import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components/history" as History

YDDialog {
    id: root

    dialog: "HistoryDialog"
    header: null
    background: Rectangle { color: Theme.Colors.blank }
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    standardButtons: Dialog.NoButton

    anchors.centerIn: undefined

    contentItem: History.HistoryView {}

    Connections {
        target: historyModel

        function onSizeChanged(size) {
            if (size === Theme.Size.none) {
                dialogManager.close_dialog(root.dialog)
            }
        }
    }

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "x"; from: root.x + 100; to: root.x; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; from: Theme.Visible.off; to: Theme.Visible.on; duration: Theme.Animation.quick }
        }
    }

    exit: Transition {
        ParallelAnimation {
            NumberAnimation { property: "x"; from: root.x; to: root.x + 100; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
        }
    }
}
