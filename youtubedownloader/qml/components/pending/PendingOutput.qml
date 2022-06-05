import QtQuick 2.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

Components.Output {
    id: root

    signal changeOutput(string path)

    MouseArea {
        anchors.fill: parent

        onClicked: dialogManager.openDialog("SelectDirectoryDialog", { "folder": root.itemOptions.output }, function(selectedFolder){
            let path = Paths.cleanPath(selectedFolder)

            root.changeOutput(path)
        })
    }
}
