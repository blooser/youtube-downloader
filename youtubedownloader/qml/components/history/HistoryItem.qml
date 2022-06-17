import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../link" as Link
import "../" as Components

Item {
    id: root

    property alias downloadInfo: linkInfo.info

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: 0

        Components.TileText {
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize: 10

            text: downloadInfo.date
        }

        RowLayout {
            Layout.fillWidth: true

            spacing: Theme.Margins.small

            Link.LinkInfo {
                id: linkInfo

                Layout.fillWidth: true
            }

            HistoryItemButtons {
                onRemove: historyModel.remove(downloadInfo.url)
                onInsert: Signals.emitInsert(downloadInfo.url)
            }
        }
    }
}
