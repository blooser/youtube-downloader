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
    signal redo()
    signal pause()

    implicitWidth: downloadItemInfo.implicitWidth
    implicitHeight: downloadItemInfo.implicitHeight

    from: 0
    value: downloadProgress.downloaded_bytes
    to: downloadProgress.total_bytes

    DownloadItemInfo {
        id: downloadItemInfo

        z: root.z + 1

        anchors.fill: root

        onRemove: root.remove()
        onOpen: root.open()
        onRedo: root.redo()
        onPause: root.pause()
    }

    state: "*"
    states: State {
        //when: downloadProgress.downloadStatus.includes("ERROR")
        name: "error"
        PropertyChanges { target: root; error: true }
    }

    transitions: [
        Transition {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    ]
}
