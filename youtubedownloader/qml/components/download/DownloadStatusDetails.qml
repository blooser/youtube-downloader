import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Rectangle {
    id: root

    property alias status: statusText.text
    property alias estimatedTime: estimatedTime.text
    property alias downloadedBytes: downloadedBytes.text
    property alias totalBytes: totalBytes.text
    property alias speed: speed.text

    readonly property bool downloading: (status.includes("downloading"))

    implicitWidth: mainLayout.implicitWidth + Theme.Margins.small // TODO: Use Pane
    implicitHeight: mainLayout.implicitHeight + Theme.Margins.small

    color: Theme.Colors.third
    radius: Theme.Margins.tiny

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.zero

        RowLayout {
            spacing: Theme.Margins.zero

            Layout.fillWidth: true

            visible: root.downloading

            Items.YDText {
                id: downloadedBytes
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none
                font.pixelSize: Theme.FontSize.micro
            }

            Items.YDText {
                id: totalBytes
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none
                font.pixelSize: Theme.FontSize.micro
            }
        }

        Items.YDText {
            id: statusText

            Layout.fillWidth: true
            Layout.maximumWidth: 750
        }

        RowLayout {
            spacing: Theme.Margins.zero

            Layout.fillWidth: true

            visible: root.downloading

            Items.YDText {
                id: estimatedTime
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none
                font.pixelSize: Theme.FontSize.micro
            }

            Items.YDText {
                id: speed
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none
                font.pixelSize: Theme.FontSize.micro
            }
        }
    }
}
