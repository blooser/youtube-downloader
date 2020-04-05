import QtQuick 2.14
import QtQuick.Controls 2.14

import "../items" as Items

YDDialog {
    id: root

    property alias text: textItem.text

    dialog: "ConfirmDialog"

    standardButtons: Dialog.Cancel | Dialog.Yes

    contentItem: Items.YDText {
        id: textItem
    }

    onAccepted: callback()
}
