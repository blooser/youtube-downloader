import QtQuick 2.14
import QtQuick.Controls 2.14

import "../items" as Items


YDDialog {
    id: root

    property alias text: textItem.text

    implicitWidth: 450
    implicitHeight: 200

    dialog: "ConfirmDialog"
    headerText: qsTr("Confirmation")

    standardButtons: Dialog.Cancel | Dialog.Yes

    contentItem: Items.YDText {
        id: textItem
        wrapMode: Text.WordWrap
    }

    onAccepted: callback()
}
