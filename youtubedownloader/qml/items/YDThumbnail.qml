﻿import QtQuick 2.14
import QtQuick.Controls 2.14

YDImage {
    id: root

    MouseArea {
        anchors.fill: parent
        enabled: (root.status === Image.Ready)
        onClicked: dialogManager.openDialog("ThumbnailDialog", {"url": root.source}, null)
    }
}
