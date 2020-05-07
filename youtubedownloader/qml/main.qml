import QtQuick 2.14
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.14

import Qt.labs.settings 1.1

import "items" as Items
import "components" as Components
import "components/download" as Download
import "components/link" as Link
import "util/regex.js" as Regex

ApplicationWindow {
    id: root

    width: 1050; height: 1050
    visible: true

    title: qsTr("Youtube Downloader")

    background: Rectangle {
        color: Theme.Colors.base
    }

    Settings {
        property alias x: root.x
        property alias y: root.y
        property alias width: root.width
        property alias height: root.height
    }

    ColumnLayout {
        id: mainLayout

        anchors {
            fill: parent
            margins: Theme.Margins.normal
        }

        Link.LinkInput {
            Layout.fillWidth: true

            options: downloadOptions.options
            onAddLink: downloadManager.predownload(link, downloadOptions.options)
        }

        Download.DownloadOptions {
            id: downloadOptions
            Layout.fillWidth: true

        }

        Components.Downloads {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    QtObject {
        id: predownloadDropProcess

        property var addPreDownload: function(url) {
            const pathType = Paths.getPathType(url)
            if (pathType === "remote") {
                if (Regex.isYoutubeLink(url) && !downloadManager.exists(url, downloadOptions.options)) {
                    downloadManager.predownload(url, downloadOptions.options)
                }
            } else if(pathType === "file") {
                let youtubeUrls = Regex.filterUrlsForYoutubeOnly((Paths.readFile(url)))
                for (let youtubeUrl of youtubeUrls) {
                    if (!downloadManager.exists(youtubeUrl, downloadOptions.options)) {
                        downloadManager.predownload(youtubeUrl, downloadOptions.options)
                    }
                }
            }
        }

        property var addPreDownloads: function(urls) {
            for (let url of urls) {
                addPreDownload(url)
            }
        }
    }

    DropArea {
        anchors.fill: parent
        onContainsDragChanged: {
            if (containsDrag) {
                dialogManager.open_dialog("DropUrlDialog", {}, null)
            } else {
                dialogManager.close_dialog("DropUrlDialog")
            }
        }
        onDropped: predownloadDropProcess.addPreDownloads(drop.urls)
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
                console.warn("Failed to create", url, component.errorString())
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
