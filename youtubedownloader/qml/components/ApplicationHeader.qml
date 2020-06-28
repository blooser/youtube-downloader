import QtQuick 2.14

import "../items" as Items

Items.YDToolBar {

    Row {
        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDToolButton {
            text: qsTr("Supported sites")
            onClicked: dialogManager.open_dialog("SupportedSitesDialog", {}, null)
            enabled: (supportedSitesModel.size !== Theme.Capacity.empty)
        }

        Items.YDToolButton {
            text: qsTr("History")
            enabled: (historyModel.size !== Theme.Capacity.empty)
        }
    }
}
