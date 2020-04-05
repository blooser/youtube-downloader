import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../dynamic" as Dynamic
import "../../items" as Items

Item {
    id: root

    implicitWidth: item.implicitWidth
    implicitHeight: item.implicitHeight


    DownloadItems {
        id: item
        anchors.fill: parent
    }
}
