import QtQuick 2.14

Item {
    id: root

    implicitWidth: downloadItems.implicitWidth
    implicitHeight: downloadItems.implicitHeight

    ListView {
        id: downloadItems

        anchors.fill: parent

        boundsBehavior: Flickable.StopAtBounds
        clip: true
        spacing: Theme.Margins.tiny
        model: downloadModel

        delegate: DownloadItem {
            width: downloadItems.width

            from: Theme.Size.none
            value: downloadProgress.downloadedBytes
            to: downloadProgress.totalBytes

            link: url

            downloadProgress: progress
            downloadData: download_data
            downloadOptions: options

            onPause: downloadModel.pause(index)
            onRedo: downloadModel.redo(index)
            onOpen: Qt.openUrlExternally(Paths.cleanPath("%1/%2.%3").arg(options.outputPath).arg(download_data.title).arg(options.fileFormat))
            onRemove: dialogManager.open_dialog("ConfirmDeleteDialog", {"downloadData": downloadData }, function() {
                downloadModel.remove_download(index)
            })
        }
    }

    Behavior on implicitHeight {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
