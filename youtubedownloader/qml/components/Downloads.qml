import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "predownload" as PreDownload
import "download" as Download
import "../items" as Items

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        PreDownload.PreDownloadItems {
            Layout.fillWidth: true
            Layout.preferredHeight: implicitHeight
        }

        Separator {
            visible: predownloadModel.size && downloadModel.size
        }

        Download.DownloadItems {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Items.YDText {
        anchors.centerIn: parent
        visible: !predownloadModel.size && !downloadModel.size
        text: qsTr("You can drag YouTube video's thumbnail and drop into YouTube Downloader")
        opacity: Theme.Visible.disabled
    }
}


