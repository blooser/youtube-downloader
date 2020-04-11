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
            Layout.alignment: Qt.AlignLeft
        }

        Items.YDButton {
            id: outputPath
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            text: Settings.outputPath
            onClicked: dialogManager.open_dialog("SelectDirectoryDialog", { "folder": Settings.outputPath }, function(selectedFolder){
                Settings.outputPath = paths.cleanPath(selectedFolder)
            })
        }
    }
}
