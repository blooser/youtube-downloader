import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property var downloadStatus
    property var downloadInfo
    property var downloadOptions
    property var downloadProgress

    signal remove()
    signal resume()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    from: 0
    value: downloadProgress.downloaded_bytes
    to: downloadProgress.total_bytes

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            leftMargin: Theme.Margins.normal
            rightMargin: Theme.Margins.normal
        }

        z: root.z + 1


        Link.LinkInfo {
            id: link

            Layout.fillWidth: true
            Layout.fillHeight: true

            info: root.downloadInfo
        }

        Components.TileText {
            Layout.preferredWidth: 65

            text: root.downloadStatus
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

    Components.Output {
        anchors {
            horizontalCenter: root.horizontalCenter
            bottom: root.bottom
        }

        itemOptions: root.downloadOptions
        itemInfo: root.downloadInfo
    }
}
