import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../items" as Items

Item {
    id: root

    property alias text: textItem.text

    implicitWidth: mainLayout.implicitWidth + 10
    implicitHeight: mainLayout.implicitHeight + 10

    ColumnLayout {
        id: mainLayout

        anchors {
            fill: root
            margins: 5
        }

        Items.YDText {
            id: textItem

            Layout.fillWidth: true

            font.pixelSize: Theme.FontSize.big
        }

        Separator {

        }
    }
}
