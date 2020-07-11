import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../components" as Components

Rectangle {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: Theme.Colors.base

    ColumnLayout {
        id: mainLayout

        anchors {
            fill: root
            margins: Theme.Margins.big
        }

        spacing: Theme.Margins.small

        Components.InputWithRemovableButton {
            id: searchInput

            Layout.fillWidth: true

            placeholderText: qsTr("Search")
            focus: true
        }

        HistoryItems {
            id: historyItems

            Layout.fillWidth: true
            Layout.fillHeight: true

            searchString: searchInput.text
        }
    }
}
