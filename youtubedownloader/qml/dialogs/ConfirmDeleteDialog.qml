import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../items" as Items
import "../components/link" as Link
import "../components" as Components

YDDialog {
    id: root

    property var downloadData

    implicitHeight: 220

    dialog: "ConfirmDeleteDialog"
    headerText: qsTr("Delete confirmation")

    standardButtons: Dialog.Cancel | Dialog.Yes

    contentItem: Components.Header {
        header: qsTr("Are you sure you want to delete?")

        Link.LinkInfo {
            Layout.fillWidth: true
            Layout.maximumWidth: 500

            thumbnailSource: downloadData.thumbnail
            titleText: downloadData.title
            uploaderText: downloadData.uploader
            durationText: downloadData.duration
        }
    }

    onAccepted: callback()
}
