import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../dynamic" as Dynamic

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + preDownloadItems.contentHeight // TODO: Is there another way?

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDButton {
            id: downloadButton

            Layout.alignment: Qt.AlignHCenter

            text: qsTr("Download %1 items").arg(preDownloadItems.itemsReady)
            enabled: preDownloadItems.itemsReady && !preDownloadItems.itemsProcessing

            onClicked: downloadManager.download()

            Behavior on opacity {
                OpacityAnimator {
                    duration: Theme.Animation.quick
                }
            }

            state: "hidden"
            states: State {
                name: "hidden"
                when: (preDownloadItems.itemsReady === 0)
                PropertyChanges { target: downloadButton; implicitHeight: Theme.Size.none; opacity: Theme.Visible.off }
            }

            transitions: Transition {
                ParallelAnimation {
                    NumberAnimation { property: "implicitHeight"; duration: Theme.Animation.quick }
                    OpacityAnimator { duration: Theme.Animation.quick }
                }
            }
        }

        ListView {
            id: preDownloadItems

            property int itemsNotReady: Theme.Capacity.empty
            property int itemsProcessing: Theme.Capacity.empty
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
                link: url
                linkTitle: title
                linkUploader: uploader
                linkUploaderLink: uploaderUrl
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

    Behavior on implicitHeight {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
