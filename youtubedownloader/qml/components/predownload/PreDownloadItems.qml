import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + preDownloadItems.contentHeight // TODO: Is there another way?

    state: "hidden"
    states: State {
        name: "hidden"
        when: (preDownloadItems.count === Theme.Size.none)
        PropertyChanges { target: root; implicitHeight: Theme.Size.none; opacity: Theme.Visible.off; }
    }

    transitions: Transition {
        NumberAnimation { properties: "opacity"; duration: Theme.Animation.quick }
    }

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDButton {
            id: downloadButton

            Layout.alignment: Qt.AlignHCenter

            icon.source: Resources.icons.download

            text: qsTr("Download")
            enabled: preDownloadItems.itemsReady && !preDownloadItems.itemsProcessing

            onClicked: downloadManager.download()
        }

        Components.DownloadsLabel {
            Layout.fillWidth: true

            opacity: preDownloadItems.count
            text: qsTr("To Download")
            counter: preDownloadItems.itemsReady

            Behavior on opacity {
                NumberAnimation {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: preDownloadItems

            property int itemsNotReady: Theme.Capacity.empty
            property int itemsProcessing: Theme.Capacity.empty
            readonly property int itemsReady: count - itemsNotReady - itemsProcessing

            Layout.fillWidth: true
            Layout.fillHeight: true

            boundsBehavior: Flickable.StopAtBounds
            clip: true
            spacing: Theme.Margins.tiny
            model: predownloadModel

            delegate: PreDownloadItem {
                width: preDownloadItems.width

                // TODO: Make it consistent
                property bool predownloadIsNotReady: (status === "exists")
                property bool predownloadIsProcessing: (status === "processing")
                property bool predownloadIsNotSupported: (status.includes("ERROR"))
                onPredownloadIsNotReadyChanged: preDownloadItems.itemsNotReady += (predownloadIsNotReady) ? 1 : -1
                onPredownloadIsNotSupportedChanged: preDownloadItems.itemsNotReady += (predownloadIsNotSupported) ? 1 : 0
                onPredownloadIsProcessingChanged: preDownloadItems.itemsProcessing += (predownloadIsProcessing) ? 1 : -1

                preDownloadStatus: status
                link: url

                downloadData: download_data
                downloadOptions: options
                destinationFile: destination_file

                onChangeFormat: {
                    options = { // NOTE: It will update key, not override whole options, check PreDownloadModel's setData implementation
                        "file_format": format
                    }
                }

                onChangeOutputPath: {
                    options = {
                        "output_path": path,
                    }
                }

                onRemove: {
                    if (status.includes("ready") || status.includes("exists")) {
                        dialogManager.open_dialog("ConfirmDeleteDialog", {"downloadData":  downloadData}, function() {
                            predownloadModel.remove_predownload(index)
                        })

                        return
                    }

                    predownloadModel.remove_predownload(index) // NOTE: Instant
                }

                Component.onDestruction: {
                    if (predownloadIsNotReady || predownloadIsNotSupported) {
                        preDownloadItems.itemsNotReady -= 1
                    }

                    if (predownloadIsProcessing) {
                        preDownloadItems.itemsProcessing -= 1
                    }
                }
            }

            remove: Transition {
                OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
            }

            removeDisplaced: Transition {
                NumberAnimation { property: "y"; duration: Theme.Animation.quick }
            }
        }
    }

    Behavior on implicitHeight {
        NumberAnimation {
            duration: Theme.Animation.quick
        }
    }
}
