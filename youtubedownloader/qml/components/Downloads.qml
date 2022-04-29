import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "predownload" as PreDownload
import "pending" as Pending
import "download" as Download
import "../items" as Items

Flickable {
    id: root

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
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}


