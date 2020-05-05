import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    property alias iconSource: icon.source
    property alias text: textItem.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDImage {
            id: icon

            Layout.alignment: Qt.AlignVCenter
            Layout.preferredWidth: 16
            Layout.preferredHeight: 16
        }

        Items.YDText {
            id: textItem

            Layout.fillWidth: true
        }
    }
}
