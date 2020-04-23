import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property alias statusText: downloadItemInfo.statusText
    property alias link: downloadItemInfo.link
    property alias thumbnailSrc: downloadItemInfo.thumbnailSrc
    property alias titleText: downloadItemInfo.titleText
    property alias uploaderText: downloadItemInfo.uploaderText
    property alias uploaderLink: downloadItemInfo.uploaderLink
    property alias linkDuration: downloadItemInfo.linkDuration

    property alias selectedFormat: downloadItemInfo.selectedFormat

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: downloadItemInfo.implicitWidth
    implicitHeight: downloadItemInfo.implicitHeight

    DownloadItemInfo {
        id: downloadItemInfo

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
