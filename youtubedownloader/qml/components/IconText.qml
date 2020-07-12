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
        spacing: icon.visible ? Theme.Margins.tiny : Theme.Margins.zero

        Items.YDImage {
            id: icon

            Layout.alignment: Qt.AlignVCenter
            Layout.preferredWidth: Theme.Size.iconSmall
            Layout.preferredHeight: Theme.Size.iconSmall

            visible: (textItem.text !== Theme.String.empty && icon.source.toString() !== "")
        }

        Items.YDText {
            id: textItem

            Layout.fillWidth: true
        }
    }
}
