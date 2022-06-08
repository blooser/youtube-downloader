import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../link" as Link

Item {
    id: root

    property alias downloadInfo: linkInfo.info

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.small

        Link.LinkInfo {
            id: linkInfo

            Layout.fillWidth: true
        }

        HistoryItemButtons {
            onRemove: historyModel.remove(downloadInfo.url)
        }
    }
}
