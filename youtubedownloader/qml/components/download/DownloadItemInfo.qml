﻿import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Item {
    id: root

    property var downloadStatus
    property var downloadInfo
    property var downloadOptions

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            leftMargin: Theme.Margins.normal
            rightMargin: Theme.Margins.normal
        }

        spacing: Theme.Margins.normal

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true

            info: downloadInfo
        }

        DownloadStatus {
            id: downloadStatus
            //downloadProgress: root.downloadProgress
        }

        Components.TileText {
            id: selectedFormat

            Layout.preferredWidth: 65

            text: downloadOptions.format
        }

        DownloadButtons {
           // status: root.downloadProgress.downloadStatus

            onOpen: root.open()
            onRedo: root.redo()
            onRemove: root.remove()
            onPause: root.pause()
        }
    }
}
