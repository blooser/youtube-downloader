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
        onSupportedSites: dialogManager.open_dialog("SupportedSitesDialog", {}, null)
        onHistory: dialogManager.open_dialog("HistoryDialog", {
                                                "x": root.width - (root.width/2),
                                                "implicitWidth": root.width/2,
                                                "implicitHeight": root.height
                                             }, null)
        onTheme: dialogManager.open_dialog("ThemeColorsDialog", {
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
            onAddTab: downloadManager.predownload(url, downloadOptions.options)
        }

        Link.LinkInput {
            Layout.fillWidth: true

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

        function onOpen(dialog, properties, callback) { dialogCreator.open(dialog, properties, callback) }
        function onClose(dialog) { dialogCreator.close(dialog) }
    }
}
