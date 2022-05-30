import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Rectangle {
    id: root

    property var downloadProgress
    property var downloadStatus

    implicitWidth: mainLayout.implicitWidth + Theme.Margins.big // TODO: Use Pane
    implicitHeight: mainLayout.implicitHeight + Theme.Margins.big

    color: Theme.Colors.third
    radius: Theme.Margins.tiny

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.tiny

        RowLayout {
            spacing: Theme.Margins.zero

            Layout.fillWidth: true

            Items.YDText {
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none

                font.pixelSize: Theme.FontSize.micro

                text: downloadProgress._eta_str
            }

            Items.YDText {
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none

                font.pixelSize: Theme.FontSize.micro

                text: downloadProgress._percent_str
            }
        }

        Items.YDText {
            Layout.fillWidth: true
            Layout.maximumWidth: 750

            font.pixelSize: Theme.FontSize.micro

            text: qsTr("%1 %2").arg(downloadStatus).arg(Paths.getFileType(downloadProgress.filename))
        }

        RowLayout {
            spacing: Theme.Margins.zero

            Layout.fillWidth: true

            Items.YDText {
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none

                font.pixelSize: Theme.FontSize.micro

                text: downloadProgress._speed_str
            }

            Items.YDText {
                Layout.fillWidth: true
                Layout.preferredWidth: Theme.Size.none

                font.pixelSize: Theme.FontSize.micro

                text: downloadProgress._total_bytes_str
            }
        }
    }
}
