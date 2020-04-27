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
            value: downloadProgress.downloadedBytes
            to: downloadProgress.totalBytes

            link: url

            downloadProgress: progress
            downloadData: download_data
            downloadOptions: options

            onPause: downloadModel.pause(index)
            onRedo: downloadModel.redo(index)
            onOpen: Qt.openUrlExternally(Paths.cleanPath("%1/%2.%3").arg(options.outputPath).arg(download_data.title).arg(options.fileFormat))
            onRemove: dialogManager.open_dialog("ConfirmDialog", {"text": qsTr("Are you sure you want to delete <b>%1</b> by <b>%2</b>?".arg(download_data.title).arg(download_data.uploader))}, function() {
                downloadModel.remove_download(index)
            })
        }
    }

    Behavior on implicitHeight {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
