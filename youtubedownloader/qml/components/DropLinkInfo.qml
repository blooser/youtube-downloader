import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDText {
            Layout.fillWidth: true

            text: qsTr("Drop your mouse to add new video to download")

            font.pixelSize: Theme.FontSize.big
            font.bold: true

            style: Text.Sunken
            styleColor: Theme.Colors.base
        }

        Items.YDImage {
            Layout.preferredWidth: 84
            Layout.preferredHeight: 84
            Layout.alignment: Qt.AlignHCenter

            source: Resources.icons.arrowDown
        }
    }
}
