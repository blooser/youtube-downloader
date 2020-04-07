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
            value: downloadedBytes
            to: totalBytes

            statusText: status
            thumbnailSrc: thumbnail
            titleText: title
            uploaderText: uploader
            linkDuration: duration

            selectedFormat: type

            onOpen: Qt.openUrlExternally(paths.cleanPath("%1/%2.%3").arg(output_path).arg(title).arg(type))
            onRemove: downloadModel.remove_download(index)
        }
    }
}
