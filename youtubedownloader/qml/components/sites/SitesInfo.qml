import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../components" as Components

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.big

        Components.InputWithRemovableButton {
            id: siteInput

            Layout.fillWidth: true

            placeholderText: qsTr("Search site")
            focus: true
        }

        Sites {
            Layout.fillWidth: true
            Layout.fillHeight: true

            site: siteInput.text
        }
    }
}
