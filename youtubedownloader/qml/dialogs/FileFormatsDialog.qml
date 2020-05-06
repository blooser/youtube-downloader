import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

import "../items" as Items
import "../components/format" as Format
import "../components/link" as Link
import "../components" as Components

YDDialog {
    id: root

    property string format

    dialog: "FileFormatsDialog"
    headerText: qsTr("File formats")

    standardButtons: Dialog.Ok

    implicitWidth: 650

    contentItem: Format.FormatFileDescriptions {
        id: formatFileDescriptions
    }

    Component.onCompleted: {
        if (format) {
            formatFileDescriptions.setFormat(format)
        }
    }

    Behavior on implicitHeight {
        NumberAnimation { duration: Theme.Animation.quick }
    }
}
