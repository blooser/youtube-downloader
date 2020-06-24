import QtQuick 2.14

import "../items" as Items

Items.YDToolBar {

    Items.YDToolButton {
        text: qsTr("Supported sites")
        onClicked: dialogManager.open_dialog("SupportedSitesDialog", {}, null)
    }
}
