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
        "file_format": Settings.fileFormat,
        "output_path": Settings.outputPath
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        Format.FormatFile {
            id: fileFormat

            Layout.alignment: Qt.AlignHCenter

            onFileFormatChanged: {
                Settings.fileFormat = fileFormat
                options["file_format"] = fileFormat
            }
        }

        Path.PathButton {
            id: outputPath
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignCenter
            onClicked: dialogManager.open_dialog("SelectDirectoryDialog", { "folder": Settings.outputPath }, function(selectedFolder){
                let path = Paths.cleanPath(selectedFolder)
                Settings.outputPath = path
                options["output_path"] = path
            })
        }
    }
}
