import QtQuick 2.15
import QtQuick.Dialogs
import Qt.labs.platform

FolderDialog {
    id: root

    property var callback: null

    title: qsTr("Select directory")

    // TODO: Fix that because of no currentFolder property found
    currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]

    onAccepted: () => {
        callback(root.folder)
    }
}
