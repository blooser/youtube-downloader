import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property alias downloadStatus: downloadItemInfo.downloadStatus
    property alias downloadInfo: downloadItemInfo.downloadInfo
    property alias downloadOptions: downloadItemInfo.downloadOptions

    property var downloadProgress

    signal remove()
    signal open()
    signal resume()
    signal pause()

    implicitWidth: downloadItemInfo.implicitWidth
    implicitHeight: downloadItemInfo.implicitHeight

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

        DownloadItemInfo {
            Layout.fillWidth: true
            Layout.fillHeight: true

            id: downloadItemInfo
        }

        DownloadButtons {
            Layout.preferredWidth: implicitWidth
           // status: root.downloadProgress.downloadStatus

            onOpen: root.open()
            onResume: root.resume()
            onRemove: root.remove()
            onPause: root.pause()
        }
    }
}
