import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components


Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + pending.contentHeight

    ColumnLayout {
        id: mainLayout
        spacing: Theme.Margins.tiny

        anchors.fill: parent

        Components.DownloadsLabel {
            Layout.fillWidth: true

            text: qsTr("Pending")
            counter: pending.count

            Behavior on opacity {
                NumberAnimation {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: pending

            Layout.fillWidth: true
            Layout.fillHeight: true

            boundsBehavior: Flickable.StopAtBounds
            clip: true
            spacing: Theme.Margins.tiny
            model: downloadManager.pendingModel

            add: Transition {
                OpacityAnimator { from: Theme.Visible.off; to: Theme.Visible.on; duration: Theme.Animation.quick }
            }

            delegate: PendingItem {
                width: pending.width

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

                onRemove: {
                    dialogManager.openDialog("ConfirmDeleteDialog", { "info": info }, () => {
                        downloadManager.pendingModel.remove(index)
                    })
                }
            }
        }
    }
}
