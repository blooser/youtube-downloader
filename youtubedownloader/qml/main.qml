import QtQuick 2.14
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.14

import "items" as Items
import "components" as Components
import "components/download" as Download
import "components/link" as Link

ApplicationWindow {
    id: root

    width: 1050; height: 750
    visible: true

    title: qsTr("Youtube downloader")

    background: Rectangle {
        color: Theme.Colors.base
    }

    ColumnLayout {
        id: mainLayout

        anchors {
            fill: parent
            margins: Theme.Margins.normal
        }

        Link.LinkInput {
            Layout.fillWidth: true

            onAddLink: downloadManager.predownload(link, downloadOptions.options)
        }

        Download.DownloadOptions {
            id: downloadOptions
            Layout.fillWidth: true

        }

        Components.DownloadsView {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Connections {
        target: dialogManager

        onOpen: dialogCreator.open(dialog, properties, callback)
        onClose: dialogCreator.close(dialog)
    }

    QtObject {
        id: dialogCreator

        property var dialogStack: []

        function open(url, properties, callback) {
            var component = Qt.createComponent(url)
            if (component.status === Component.Error) {
                console.warn("Failed to create", url)
                return
            }

            if (typeof callback === "function") {
                properties["callback"] = callback
            }

            var dialog = component.createObject(root, properties)
            dialog.open()

            dialogStack.push(dialog)
        }

        function close(dialog) {
            var foundDialog = dialogStack.find(item => item.dialog === dialog)

            if (foundDialog !== undefined) {
                dialogStack = dialogStack.filter(item => item.dialog !== foundDialog.dialog)
                foundDialog.close()
                foundDialog.destroy()
            }
        }
    }
}
