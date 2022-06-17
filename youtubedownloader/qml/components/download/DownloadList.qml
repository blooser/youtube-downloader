import QtQuick 2.14

import QtQuick.Layouts 1.14

import ".." as Components
import "../../items" as Items

Components.List {
    id: root

    label: qsTr("Download")
    model: downloadManager.downloadModel

    delegate: DownloadItem {
        width: root.width

        downloadStatus: status
        downloadInfo: info
        downloadOptions: options
        downloadProgress: progress

        onRemove: {
            dialogManager.openDialog("ConfirmDeleteDialog", { "info": info }, () => {
                downloadManager.downloadModel.remove(index)
            })
        }

        onResume: downloadManager.downloadModel.resume(index)
        onPause: downloadManager.downloadModel.pause(index)
        onOpen: {
            const path = Paths.pathTo(options.output, info.title, options.format)

            Qt.openUrlExternally(path)
        }
    }
}
