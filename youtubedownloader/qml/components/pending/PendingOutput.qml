import QtQuick 2.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components

Rectangle {
    id: root

    property var pendingOptions
    property var pendingInfo

    signal changeOutput(string path)

    implicitWidth: output.implicitWidth
    implicitHeight: output.implicitHeight

    color: Theme.Colors.base
    radius: 5

    Items.YDText {
        id: output

        font.pixelSize: Theme.FontSize.micro

        padding: Theme.Size.borderBold

        text: qsTr("%1/%2.%3").arg(root.pendingOptions.output)
                              .arg(root.pendingInfo.title)
                              .arg(root.pendingOptions.format)
    }

    MouseArea {
        anchors.fill: parent

        onClicked: dialogManager.openDialog("SelectDirectoryDialog", { "folder": root.pendingOptions.output }, function(selectedFolder){
            let path = Paths.cleanPath(selectedFolder)

            root.changeOutput(path)
        })
    }
}
