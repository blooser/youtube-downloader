import QtQuick 2.15
import Qt.labs.platform


FileDialog {
    id: root

    property var callback: null

    currentFile: "thumbnail"
    title: qsTr("Select file")
    folder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
    fileMode: FileDialog.SaveFile

    onAccepted: () => {
        callback(root.file)
    }
}
