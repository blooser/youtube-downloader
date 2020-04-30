import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components" as Components

YDDialog {
    id: root

    dialog: "DropUrlDialog"

    header: null
    footer: null
    standardButtons: Dialog.NoButton
    background: null

    contentItem: Components.DropUrlInfo {}
}
