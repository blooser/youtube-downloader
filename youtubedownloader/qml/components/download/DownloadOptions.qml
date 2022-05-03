import QtQuick 2.14
import QtQuick.Layouts 1.14

import Qt.labs.platform 1.1

import "../../items" as Items
import "../format" as Format
import "../path" as Path
import ".." as Components

Item {
    id: root

    property var options: {
        "format": Settings.format,
        "output": Settings.output
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        Format.FormatFile {
            id: fileFormat

            Layout.alignment: Qt.AlignHCenter

            onFileFormatChanged: (fileFormat) => {
                Settings.format = fileFormat
                options["format"] = fileFormat
            }
        }

        Path.PathButton {
            id: outputPath
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignCenter
            onClicked: dialogManager.openDialog("SelectDirectoryDialog", { "folder": Settings.output }, function(selectedFolder){
                let path = Paths.cleanPath(selectedFolder)

                Settings.output = path
                options["output"] = path
            })
        }
    }
}
