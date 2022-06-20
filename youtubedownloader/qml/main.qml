import QtQuick 2.14
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.14

import Qt.labs.settings 1.1

import "items" as Items
import "components" as Components
import "components/download" as Download
import "components/link" as Link
import "components/browser" as Browser
import "components/history" as History
import "util/regex.js" as Regex
import "util/object.js" as Object

ApplicationWindow {
    id: root

    width: 1050; height: 1050
    visible: true

    title: qsTr("Youtube Downloader")

    header: Components.ApplicationHeader {
        onSupportedSites: dialogManager.openDialog("SupportedSitesDialog", {}, null)
        onHistory: dialogManager.openDialog("HistoryDialog", {
                                                "x": root.width - (root.width/2),
                                                "implicitWidth": root.width/2,
                                                "implicitHeight": root.height
                                             }, null)
        onTheme: dialogManager.openDialog("ThemeColorsDialog", {
                                                "x": 0,
                                                "y": root.height,
                                                "implicitWidth": root.width,
                                           }, null)
    }

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

        Browser.Browsers {
            Layout.fillWidth: true

            visible: (WebBrowsers.browsers.length !== Theme.Capacity.empty)
            options: downloadOptions.options

            onAddTab: url => { downloadManager.insert(url, downloadOptions.options) }

        }

        Link.LinkInput {
            Layout.fillWidth: true

            onAddLink: link => {
                    if (Regex.isUrl(link)) {
                        downloadManager.insert(link, downloadOptions.options)
                 }
            }
        }

        Download.DownloadOptions {
            id: downloadOptions

            Layout.fillWidth: true
        }

        Components.DownloadButton {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            ready: downloads.pendingItems

            onDownload: downloadManager.download() // Let's go!
        }

        Components.Downloads {
            id: downloads

            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Items.YDText {
        anchors.centerIn: parent

        opacity: downloads.downloadItems || downloads.pendingItems ? Theme.Visible.off : Theme.Visible.disabled

        text: "Drag youtube's thumbnail and drop in youtube downloader's area"
    }

    DropArea {
        anchors.fill: parent
        onContainsDragChanged: {
            if (containsDrag) {
                dialogManager.openDialog("DropUrlDialog", {}, null)
            } else {
                dialogManager.closeDialog("DropUrlDialog")
            }
        }

        onDropped: (drop) => {
               for (const droppedUrl of drop.urls) {
                   if (Regex.isUrl(droppedUrl.toString()))
                       downloadManager.insert(droppedUrl, downloadOptions.options)
            }
        }
    }

    Connections {
        target: Signals

        function onInsert(url) {
            downloadManager.insert(url, downloadOptions.options)
        }
    }

    QtObject {
            id: dialogCreator

            property var dialogStack: []

            function open(url, properties, callback) {
                let dialog = Object.createComponent(url, root, properties, callback)

                dialog.open()

                dialogStack.push(dialog)
            }

            function close(dialog) {
                let foundDialog = dialogStack.find(item => item.dialog === dialog)

                if (foundDialog !== undefined) {
                    dialogStack = dialogStack.filter(item => item.dialog !== foundDialog.dialog)

                    foundDialog.close()
                    foundDialog.destroy()
                }
            }
        }

    Connections {
        target: dialogManager

        function onOpen(dialog, properties, callback) { dialogCreator.open(dialog, properties, callback) }
        function onClose(dialog) { dialogCreator.close(dialog) }
    }
}
