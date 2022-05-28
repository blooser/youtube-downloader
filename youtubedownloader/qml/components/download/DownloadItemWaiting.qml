import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components


Rectangle {
    property alias downloadStatus: downloadItemInfo.downloadStatus
    property alias downloadInfo: downloadItemInfo.downloadInfo
    property alias downloadOptions: downloadItemInfo.downloadOptions

    implicitWidth: downloadItemInfo.implicitWidth
    implicitHeight: downloadItemInfo.implicitHeight

    opacity: Theme.Visible.disabled
    color: Theme.Colors.second

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
    }
}

