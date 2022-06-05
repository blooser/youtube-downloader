import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import "../link" as Link
import ".." as Components

import youtubedownloader.component.changer


Rectangle {
    id: root

    property var downloadStatus
    property var downloadInfo
    property var downloadOptions

    signal remove()
    signal resume()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: Theme.Colors.error
    opacity: Theme.Colors.disabled

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            leftMargin: Theme.Margins.normal
            rightMargin: Theme.Margins.normal
        }

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true
            Layout.fillHeight: true

            info: root.downloadInfo
        }

        Components.TileText {
            Layout.preferredWidth: 65

            text: root.downloadOptions.format
        }

        DownloadButtons {
            Layout.preferredWidth: implicitWidth

            buttonsPolicy: buttons.DELETE

            onRemove: root.remove()
            onResume: root.resume()
        }
    }

    Items.YDText {
        anchors.centerIn: root

        text: info.error
    }
}


