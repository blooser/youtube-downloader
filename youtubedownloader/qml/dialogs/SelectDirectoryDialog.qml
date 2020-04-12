import QtQuick 2.14
import QtQuick.Dialogs 1.3

FileDialog {
    id: root

    property var callback: null

    selectMultiple: false
    selectExisting: true
    selectFolder: true

    title: qsTr("Select directory")

    onAccepted: callback(folder)
}
