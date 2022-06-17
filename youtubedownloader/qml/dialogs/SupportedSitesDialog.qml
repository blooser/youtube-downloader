import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../components/sites" as Sites

YDDialog {
    id: root

    implicitWidth: 800
    implicitHeight: 600

    dialog: "SupportedSitesDialog"
    headerText: qsTr("Supported sites")

    standardButtons: Dialog.Ok

    contentItem: Sites.SitesInfo {

    }
}
