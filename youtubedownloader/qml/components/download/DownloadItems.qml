import QtQuick 2.14

import QtQuick.Layouts 1.14

import ".." as Components

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.tiny

        Components.TileText {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            opacity: downloadItems.count
            text: "Downloads"

            Behavior on opacity {
                NumberAnimation {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: downloadItems

            Layout.fillWidth: true
            Layout.fillHeight: true

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
                destinationFile: destination_file

                downloadProgress: progress
                downloadData: download_data
                downloadOptions: options

                onPause: downloadModel.pause(index)
                onRedo: downloadModel.redo(index)
                onOpen: Qt.openUrlExternally(destination_file)
                onRemove: dialogManager.open_dialog("ConfirmDeleteDialog", {"downloadData": downloadData }, function() {
                    downloadModel.remove_download(index)
                })
            }

            remove: Transition {
                OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
            }

            removeDisplaced: Transition {
                NumberAnimation { property: "y"; duration: Theme.Animation.quick }
            }
        }

        Behavior on implicitHeight {
            NumberAnimation { duration: Theme.Animation.quick }
        }

    }
}
