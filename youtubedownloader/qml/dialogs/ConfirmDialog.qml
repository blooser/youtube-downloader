import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../items" as Items
import "../components/link" as Link

YDDialog {
    id: root

    property var downloadData

    implicitHeight: 220

    dialog: "ConfirmDialog"
    headerText: qsTr("Confirmation")

    standardButtons: Dialog.Cancel | Dialog.Yes

    contentItem: ColumnLayout {
        spacing: Theme.Margins.tiny

        Items.YDText {
            Layout.fillWidth: true

            text: qsTr("Are you sure you want to delete?")
            font.bold: true
        }

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
