import QtQuick 2.14

Item {
    id: root

    implicitWidth: downloadItems.implicitWidth
    implicitHeight: downloadItems.implicitHeight

    ListView {
        id: downloadItems

        anchors {
            fill: parent
            margins: Theme.Margins.tiny
        }

        clip: true
        spacing: Theme.Margins.tiny
        model: downloadModel

        delegate: DownloadItem {
            width: downloadItems.width

            from: 0
            value: progress.downloadedBytes
            to: progress.totalBytes

            statusText: progress.downloadStatus
            thumbnailSrc: thumbnail
            titleText: title
            uploaderText: uploader
            linkDuration: duration

            selectedFormat: options.downloadFormat

            onOpen: Qt.openUrlExternally(paths.cleanPath("%1/%2.%3").arg(options.outputPath).arg(title).arg(options.downloadFormat))
            onRemove: downloadModel.remove_download(index)
        }
    }
}
