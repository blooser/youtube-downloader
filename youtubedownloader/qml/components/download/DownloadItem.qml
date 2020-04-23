import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property alias statusText: preDownloadItemInfo.statusText
    property alias thumbnailSrc: preDownloadItemInfo.thumbnailSrc
    property alias titleText: preDownloadItemInfo.titleText
    property alias uploaderText: preDownloadItemInfo.uploaderText
    property alias linkDuration: preDownloadItemInfo.linkDuration

    property alias selectedFormat: preDownloadItemInfo.selectedFormat

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: preDownloadItemInfo.implicitWidth
    implicitHeight: preDownloadItemInfo.implicitHeight

    DownloadItemInfo {
        id: preDownloadItemInfo

        z: root.z + 1

        anchors {
            fill: root
            leftMargin: Theme.Margins.small
            rightMargin: Theme.Margins.small
        }

        onRemove: root.remove()
        onOpen: root.open()
        onRedo: root.redo()
        onPause: root.pause()
    }
}
