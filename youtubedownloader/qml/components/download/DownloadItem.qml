import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property alias link: downloadItemInfo.link

    property alias downloadProgress: downloadItemInfo.downloadProgress
    property alias downloadData: downloadItemInfo.downloadData
    property alias downloadOptions: downloadItemInfo.downloadOptions

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: downloadItemInfo.implicitWidth
    implicitHeight: downloadItemInfo.implicitHeight

    DownloadItemInfo {
        id: downloadItemInfo

        z: root.z + 1

        anchors {
            fill: root
            leftMargin: Theme.Margins.small
            rightMargin: Theme.Margins.small
        }

        onRemove: root.remove()
        onOpen: root.open()
        onRedo: root.redo()
        onPause: root.pause()
    }

    state: "*"
    states: State {
        when: downloadProgress.downloadStatus.includes("ERROR")
        name: "error"
        PropertyChanges { target: root; backgroundColor: Theme.Colors.error }
    }

    transitions: [
        Transition {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    ]
}
