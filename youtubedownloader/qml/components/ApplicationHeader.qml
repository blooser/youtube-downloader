import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Items.YDToolBar {
    id: root

    signal supportedSites()
    signal history()
    signal theme()

    RowLayout {
        anchors.fill: parent
        spacing: Theme.Margins.big

        Row {
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

            Items.YDToolButton {
                text: qsTr("Theme")
                onClicked: root.theme()
            }
        }

        Items.YDText {
            Layout.alignment: Qt.AlignRight
            Layout.rightMargin: Theme.Margins.big

            font.pixelSize: Theme.FontSize.micro
            text: qsTr("Version %1").arg(Qt.application.version)
        }
    }
}
