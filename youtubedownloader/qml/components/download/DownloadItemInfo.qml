import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Item {
    id: root

    property alias statusText: downloadStatus.status
    property alias thumbnailSrc: thumbnail.source
    property alias titleText: link.titleText
    property alias uploaderText: link.uploaderText
    property alias linkDuration: link.durationText

    property alias selectedFormat: selectedFormat.text

    signal remove()
    signal open()
    signal redo()
    signal pause()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: root

        spacing: Theme.Margins.normal

        Items.YDImage {
            id: thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86
        }

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true
        }

        DownloadStatus {
            id: downloadStatus
        }

        Components.TileText {
            id: selectedFormat

            Layout.preferredWidth: 65
        }

        DownloadButtons {
            status: statusText

            onOpen: root.open()
            onRedo: root.redo()
            onRemove: root.remove()
            onPause: root.pause()
        }
    }

    state: "*"
    states: State {
        when: statusText.includes("ERROR")
        name: "error"
        PropertyChanges { target: root; backgroundColor: Theme.Colors.error }
    }

    transitions: [
        Transition {
            ColorAnimation { duration: Theme.Animation.quick }
        }
    ]
}
