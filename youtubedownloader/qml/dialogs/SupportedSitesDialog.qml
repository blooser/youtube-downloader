import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components/sites" as Sites

YDDialog {
    id: root

    implicitWidth: 600
    implicitHeight: 500

    dialog: "SupportedSitesDialog"
    headerText: qsTr("Supported sites (%1)").arg(sitesInfo.sitesCount)

    standardButtons: Dialog.Ok

    contentItem: Sites.SitesInfo {
        id: sitesInfo
    }
}
