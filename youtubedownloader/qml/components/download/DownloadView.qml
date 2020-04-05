import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../dynamic" as Dynamic
import "../../items" as Items

Item {
    id: root

    implicitWidth: changer.implicitWidth
    implicitHeight: changer.implicitHeight

    Dynamic.Changer {
        id: changer

        anchors.fill: parent

        main: DownloadItems {

        }

        second: null

        when: (downloadModel.rowCount() === 0)
    }
}
