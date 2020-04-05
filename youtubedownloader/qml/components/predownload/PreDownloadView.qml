import QtQuick 2.14

import "../dynamic" as Dynamic
import ".." as Components

Item {
    id: root

    implicitWidth: changer.implicitWidth
    implicitHeight: changer.implicitHeight

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        main: PreDownloadItems {

        }

        second: null

        when: (predownloadModel.rowCount() === 0)
    }
}
