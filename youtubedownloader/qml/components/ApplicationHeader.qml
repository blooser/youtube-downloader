import QtQuick 2.14

import "../items" as Items

Items.YDToolBar {
    id: root

    signal supportedSites()
    signal history()

    Row {
        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDToolButton {
            text: qsTr("Supported sites")
            enabled: (supportedSitesModel.size !== Theme.Capacity.empty)
            onClicked: root.supportedSites()
        }

        Items.YDToolButton {
            text: qsTr("History")
            enabled: (historyModel.size !== Theme.Capacity.empty)
            onClicked: root.history()
        }
    }
}
