import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components/history" as History

YDDialog {
    id: root

    implicitWidth: 800

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
}
