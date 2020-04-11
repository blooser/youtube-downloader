import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

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

            delegate: PreDownloadItem {
                width: preDownloadItems.width

                linkTitle: title
                linkUploader: uploader
                linkDuration: duration

                thumbnailUrl: thumbnail
                selectedFormat: options.downloadFormat

                onRemove: predownloadModel.remove_predownload(index)
            }
        }
    }
}
