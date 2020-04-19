import QtQuick 2.14
import QtQuick.Layouts 1.14

import Qt.labs.platform 1.1

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property var options: {
        "file_format": Settings.fileFormat,
        "output_path": Settings.outputPath
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Components.FileFormat {
            id: fileFormat

            Layout.alignment: Qt.AlignLeft

            onFileFormatChanged: {
                Settings.fileFormat = fileFormat
                options["file_format"] = fileFormat

                root.optionsChanged()
            }
        }

        Items.YDButton {
            id: outputPath
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            text: Settings.outputPath
            onClicked: dialogManager.open_dialog("SelectDirectoryDialog", { "folder": Settings.outputPath }, function(selectedFolder){
                var path = paths.cleanPath(selectedFolder)
                Settings.outputPath = path
                options["output_path"] = path

                root.optionsChanged()
            })
        }
    }
}
