import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "predownload" as PreDownload
import "pending" as Pending
import "download" as Download
import "../items" as Items

Flickable {
    id: root

    property int pendingItems: pending.items
    property int downloadItems: download.items

    implicitHeight: mainLayout.implicitHeight
    contentHeight: implicitHeight

    clip: true
    boundsBehavior: Flickable.StopAtBounds

    ScrollBar.vertical: Items.YDScrollBar {}

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Pending.PendingList {
            id: pending

            Layout.fillWidth: true
            //Layout.fillHeight: true
        }

        Download.DownloadList {
            id: download

            Layout.fillWidth: true
            //Layout.fillHeight: true
        }
    }
}


