import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components


Components.List {
    id: root

    model: downloadManager.pendingModel
    label: qsTr("Pending")

    delegate: PendingItem {
        width: root.width

        pendingStatus: status
        pendingInfo: info
        pendingOptions: options

        // TODO: Move this logic into class or special function
        onFormatSelected: format => {
            options = {
                "format": format,
                "output": options.output,
            }
        }

        onChangeOutput: path => {
            options = {
                "format": options.format,
                "output": path
            }
        }

        onForceRemove: downloadManager.pendingModel.remove(index)
        onRemove: {
            dialogManager.openDialog("ConfirmDeleteDialog", { "info": info }, () => {
                downloadManager.pendingModel.remove(index)
            })
        }
    }
}
