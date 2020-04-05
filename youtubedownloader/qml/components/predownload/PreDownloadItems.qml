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
                    duration: 250
                }
            }
        }

        ListView {
            id: preDownloadItems

            Layout.fillWidth: true
            Layout.fillHeight: true

            clip: true
            model: predownloadModel

            delegate: PreDownloadItem {
                width: preDownloadItems.width

                linkTitle: title
                linkUploader: uploader
                thumbnailUrl: thumbnail
                selectedFormat: type

                onRemove: predownloadModel.remove_predownload(index)
            }
        }
    }
}
