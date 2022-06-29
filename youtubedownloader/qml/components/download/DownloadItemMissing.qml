import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import "../link" as Link
import ".." as Components


Rectangle {
    id: root

    property var downloadStatus
    property var downloadInfo
    property var downloadOptions

    signal remove()
    signal resume()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    opacity: Theme.Visible.disabled
    color: Theme.Colors.error

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

            info: downloadInfo
        }

        Components.TileText {
            Layout.preferredWidth: 65

            text: "missing"
        }

        Components.Spacer {

        }

        Components.TileText {
            Layout.preferredWidth: 65

            text: root.downloadOptions.format
        }

        Components.Spacer {

        }

        DownloadButtons {
            Layout.preferredWidth: implicitWidth

            buttonsPolicy: buttons.RESUME | buttons.DELETE

            onResume: root.resume()
            onRemove: root.remove()
        }
    }
}

