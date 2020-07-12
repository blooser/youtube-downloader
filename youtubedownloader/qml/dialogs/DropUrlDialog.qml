import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components" as Components

YDDialog {
    id: root

    dialog: "DropUrlDialog"

    modal: false
    dim: true

    Overlay.modeless: Rectangle {
        color: "#99000000"

        Behavior on opacity {
            OpacityAnimator { duration: 250 }
        }
    }

    header: null
    footer: null
    standardButtons: Dialog.NoButton
    background: null

    contentItem: Components.DropUrlInfo {}
}
