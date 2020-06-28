import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../link" as Link

Item {
    id: root

    property alias link: linkInfo.link
    property alias titleText: linkInfo.titleText
    property alias uploaderText: linkInfo.uploaderText
    property alias uploaderLink: linkInfo.uploaderLink
    property alias thumbnailSource: linkInfo.thumbnailSource

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
            onRemove: historyModel.remove(link)
            onAdd: downloadManager.preDownloadRequest(link)
        }
    }
}
