import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components" as Components
import "../items" as Items

YDDialog {
    id: root

    property string url

    dialog: "ThumbnailDialog"

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    header: null
    footer: null
    standardButtons: Dialog.NoButton
    contentItem: Items.YDImage {
        source: root.url

        MouseArea {
            anchors.fill: parent
            onClicked: root.close()
        }
    }
}
