import QtQuick 2.14
import QtQuick.Layouts 1.14

import Qt.labs.platform 1.1

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property var options: {
        "type": format.format,
        "output_path": outputPath.text
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Components.Format {
            id: format

            Layout.alignment: Qt.AlignLeft
        }

        Items.YDButton {
            id: outputPath
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            text: paths.cleanPath(StandardPaths.writableLocation(StandardPaths.DownloadLocation))
            onClicked: dialogManager.open_dialog("SelectDirectoryDialog", {"folder": StandardPaths.writableLocation(StandardPaths.DownloadLocation)}, function(selectedFolder){
                text = paths.cleanPath(selectedFolder)
            })
        }
    }
}
