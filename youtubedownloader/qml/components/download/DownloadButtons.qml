import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Item {
   id: root

   property string status: "queued"

   signal open()
   signal redo()
   signal pause()
   signal remove()

   implicitWidth: mainLayout.implicitWidth
   implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDImageButton {
            id: downloadButton

            Layout.alignment: Qt.AlignRight
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }

    state: "queued"
    states: [
        State {
            when: status.includes("ERROR")
            name: "error"
            PropertyChanges { target: downloadButton; implicitWidth: Theme.Size.icon; implicitHeight: Theme.Size.icon; opacity: Theme.Visible.on; imageSource: Resources.icons.redo; onClicked: root.redo() }
        },

        State {
            when: (status === "queued")
            name: "queued"
            PropertyChanges { target: downloadButton; implicitWidth: Theme.Size.none; implicitHeight: Theme.Size.none; opacity: Theme.Visible.off }
        },

        State {
            when: (status === "downloading")
            name: "downloading"
            PropertyChanges { target: downloadButton; imageSource: Resources.icons.pause; enabled: true; implicitWidth: Theme.Size.icon; implicitHeight: Theme.Size.icon; onClicked: root.pause() }
        },

        State {
            when: (status === "paused")
            name: "paused"
            PropertyChanges { target: downloadButton; imageSource: Resources.icons.redo; implicitWidth: Theme.Size.icon; implicitHeight: Theme.Size.icon; onClicked: root.redo() }
        },


        State {
            when: status.includes("converting")
            name: "converting"
            PropertyChanges { target: downloadButton; implicitWidth: Theme.Size.none; implicitHeight: Theme.Size.none; opacity: Theme.Visible.off }
        },

        State {
            when: (status === "finished")
            name: "finished"
            PropertyChanges { target: downloadButton; imageSource: Resources.icons.folder; implicitWidth: Theme.Size.icon; implicitHeight: Theme.Size.icon; opacity: Theme.Visible.on; onClicked: root.open() }
        }
    ]

    transitions: Transition {
        SequentialAnimation {
            NumberAnimation { properties: "implicitWidth, implicitHeight"; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; duration: Theme.Animation.quick }
        }
    }
}
