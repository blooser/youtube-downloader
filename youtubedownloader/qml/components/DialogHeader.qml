import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../items" as Items

Item {
    id: root

    property alias text: textItem.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDText {
            id: textItem

            Layout.fillWidth: true

            font.pixelSize: Theme.FontSize.big
        }

        Separator {

        }
    }
}
