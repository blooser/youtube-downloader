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
            link: url
            titleText: title
            uploaderText: uploader
            uploaderLink: uploaderUrl
            linkDuration: duration

            selectedFormat: options.fileFormat

            onPause: downloadModel.pause(index)
            onRedo: downloadModel.redo(index)
            onOpen: Qt.openUrlExternally(paths.cleanPath("%1/%2.%3").arg(options.outputPath).arg(title).arg(options.fileFormat))
            onRemove: dialogManager.open_dialog("ConfirmDialog", {"text": qsTr("Are you sure you want to delete <b>%1</b> by <b>%2</b>?".arg(title).arg(uploader))}, function(){
                downloadModel.remove_download(index)
            })
        }
    }
}
