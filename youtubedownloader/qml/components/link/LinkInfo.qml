import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property alias titleText: title.text
    property alias uploaderText: uploader.text
    property alias durationText: duration.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    GridLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDText {
            id: title

            Layout.row: 0
            Layout.column: 0
            Layout.columnSpan: 3
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

            font.pixelSize: Theme.FontSize.normal
            horizontalAlignment: Text.AlignLeft
        }

        Items.YDText {
            id: uploader

            Layout.row: 1
            Layout.column: 0
            Layout.alignment: Qt.AlignLeft

            horizontalAlignment: Text.AlignLeft

        }

        Items.YDText {
            id: duration

            Layout.row: 1
            Layout.column: 1
            Layout.alignment: Qt.AlignLeft

            horizontalAlignment: Text.AlignLeft
        }
    }
}
