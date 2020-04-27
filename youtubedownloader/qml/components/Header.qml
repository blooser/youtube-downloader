import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    property alias header: header.text
    default property alias contentItems: mainLayout.data

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDText {
            id: header

            Layout.fillWidth: true
            font.bold: true
        }
    }
}
