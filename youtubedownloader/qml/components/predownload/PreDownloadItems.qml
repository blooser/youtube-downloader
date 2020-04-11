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

            text: qsTr("Download %1 items").arg(preDownloadItems.count)
            opacity: preDownloadItems.count ? 1 : 0

            onClicked: downloadManager.download()

            Behavior on opacity {
                OpacityAnimator {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: preDownloadItems

            Layout.fillWidth: true
            Layout.fillHeight: true

            clip: true
            spacing: Theme.Margins.tiny
            model: predownloadModel

            delegate: Dynamic.Changer {
                width: preDownloadItems.width

                main: PreDownloadItemCollectingInfoIndicator {}

                second: PreDownloadItem {
                    linkTitle: title
                    linkUploader: uploader
                    linkDuration: duration

                    thumbnailUrl: thumbnail
                    selectedFormat: options.fileFormat

                    onRemove: dialogManager.open_dialog("ConfirmDialog", {"text": qsTr("Are you sure you want to delete <b>%1</b> by <b>%2</b>?".arg(title).arg(uploader))}, function(){
                        predownloadModel.remove_predownload(index)
                    })
                }

                when: ready
            }
        }
    }
}
