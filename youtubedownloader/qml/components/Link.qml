import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../items" as Items

Item {
    id: root

    property alias title: title.text
    property alias uploader: uploader.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDText {
            id: title

            Layout.fillWidth: true
            horizontalAlignment: Text.AlignLeft
            font.pixelSize: Theme.FontSize.normal
        }

        Items.YDText {
            id: uploader

            Layout.fillWidth: true
            horizontalAlignment: Text.AlignLeft
        }
    }
}
