import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../dynamic" as Dynamic

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDButton {
            Layout.alignment: Qt.AlignHCenter

            text: qsTr("Download %1 items").arg(preDownloadItems.itemsReady)
            opacity: preDownloadItems.itemsReady ? Theme.Visible.on : Theme.Visible.off

            enabled: preDownloadItems.itemsReady && !preDownloadItems.itemsProcessing

            onClicked: downloadManager.download()

            Behavior on opacity {
                OpacityAnimator {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: preDownloadItems

            property int itemsNotReady: 0
            property int itemsProcessing: 0
            readonly property int itemsReady: count - itemsNotReady

            Layout.fillWidth: true
            Layout.fillHeight: true

            clip: true
            spacing: Theme.Margins.tiny
            model: predownloadModel

            delegate: PreDownloadItem {
                width: preDownloadItems.width

                property bool predownloadIsNotReady: (status === "exists")
                property bool predownloadIsProcessing: (status === "processing")
                onPredownloadIsNotReadyChanged: preDownloadItems.itemsNotReady += (predownloadIsNotReady) ? 1 : -1
                onPredownloadIsProcessingChanged: preDownloadItems.itemsProcessing += (predownloadIsProcessing) ? 1 : -1

                preDownloadStatus: status
                linkTitle: title
                linkUploader: uploader
                linkDuration: duration

                thumbnailUrl: thumbnail
                selectedFormat: options.fileFormat
                destinationFile: "%1/%2.%3".arg(options.outputPath).arg(title).arg(options.fileFormat)

                onRemove: dialogManager.open_dialog("ConfirmDialog", {"text": qsTr("Are you sure you want to delete <b>%1</b> by <b>%2</b>?".arg(title).arg(uploader))}, function() {
                    predownloadModel.remove_predownload(index)
                })

                Component.onDestruction: {
                    if (predownloadIsNotReady) {
                        preDownloadItems.itemsNotReady -= 1
                    }
                }
            }
        }
    }
}
