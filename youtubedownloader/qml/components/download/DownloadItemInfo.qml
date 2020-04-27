import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Item {
    id: root

    property string link

    property var downloadProgress
    property var downloadData
    property var downloadOptions

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: root

        spacing: Theme.Margins.normal

        Items.YDImage {
            id: thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86

            source: downloadData.thumbnail
        }

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true

            link: root.link
            titleText: downloadData.title
            uploaderText: downloadData.uploader
            uploaderLink: downloadData.uploaderUrl
            durationText: downloadData.duration
        }

        DownloadStatus {
            id: downloadStatus
            downloadProgress: root.downloadProgress
        }

        Components.TileText {
            id: selectedFormat

            Layout.preferredWidth: 65

            text: downloadOptions.fileFormat
        }

        DownloadButtons {
            status: root.downloadProgress.downloadStatus

            onOpen: root.open()
            onRedo: root.redo()
            onRemove: root.remove()
            onPause: root.pause()
        }
    }
}
