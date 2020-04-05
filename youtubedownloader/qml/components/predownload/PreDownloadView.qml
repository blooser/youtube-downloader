import QtQuick 2.14

import "../dynamic" as Dynamic
import ".." as Components

Item {
    id: root

    implicitWidth: items.implicitWidth
    implicitHeight: items.implicitHeight

    PreDownloadItems {
        id: items

        anchors.fill: parent
    }
}
