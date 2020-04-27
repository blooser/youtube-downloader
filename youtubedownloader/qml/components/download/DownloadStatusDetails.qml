import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Rectangle {
    id: root

    property alias status: statusText.text
    property alias estimatedTime: estimatedTime.text
    property alias totalBytes: totalBytes.text

    implicitWidth: mainLayout.implicitWidth + Theme.Margins.small // TODO: Use Pane
    implicitHeight: mainLayout.implicitHeight  + Theme.Margins.small

    color: Theme.Colors.third
    radius: Theme.Margins.tiny

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.zero

        Items.YDText {
            id: statusText

            Layout.fillWidth: true
        }

        RowLayout {
            spacing: Theme.Margins.zero

            Layout.fillWidth: true

            visible: (status.includes("downloading"))

            Items.YDText {
                id: estimatedTime
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.preferredWidth: 0
                font.pixelSize: Theme.FontSize.tiny
            }

            Items.YDText {
                id: totalBytes
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.preferredWidth: 0
                font.pixelSize: Theme.FontSize.tiny
            }
        }
    }
}
