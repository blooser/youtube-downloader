import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

import youtubedownloader.component.changer


Rectangle {
    property alias downloadStatus: downloadItemInfo.downloadStatus
    property alias downloadInfo: downloadItemInfo.downloadInfo
    property alias downloadOptions: downloadItemInfo.downloadOptions

    signal remove()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: Theme.Colors.error
    opacity: Theme.Colors.disabled

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            leftMargin: Theme.Margins.normal
            rightMargin: Theme.Margins.normal
        }

        DownloadItemInfo {
            id: downloadItemInfo

            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        DownloadButtons {
            Layout.preferredWidth: implicitWidth
           // status: root.downloadProgress.downloadStatus

            onRemove: root.remove()
        }
    }
}


