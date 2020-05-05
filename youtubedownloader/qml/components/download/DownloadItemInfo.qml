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

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true

            thumbnailSource: downloadData.thumbnail
            link: root.link
            titleText: downloadData.title
            uploaderText: downloadData.uploader
            uploaderLink: downloadData.uploaderUrl
            durationText: downloadData.duration
            viewCount: downloadData.viewCount.toLocaleString(Qt.locale(), "f", 0)
            uploadDate: downloadData.uploadDate
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

    Items.YDText {
        text: "%1/%2.%3".arg(downloadOptions.outputPath).arg(downloadData.title).arg(downloadOptions.fileFormat)

        font.pixelSize: Theme.FontSize.micro
        anchors {
            bottom: root.bottom
            bottomMargin: Theme.Size.borderBold
            horizontalCenter: root.horizontalCenter
        }
    }
}
