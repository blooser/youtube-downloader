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

            Layout.preferredWidth: Theme.Size.none
            Layout.preferredHeight: Theme.Size.none
            Layout.alignment: Qt.AlignRight
            opacity: Theme.Visible.off
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }

    state: "repose"
    states: [
        State {
            when: (status.includes("ERROR") || (status === "paused"))
            name: "repose"
            PropertyChanges { target: downloadButton; Layout.preferredWidth: Theme.Size.icon; Layout.preferredHeight: Theme.Size.icon; opacity: Theme.Visible.on; imageSource: Resources.icons.redo; onClicked: root.redo() }
        },

        State {
            when: (status === "queued" || status.includes("converting"))
            name: "occupied"
            PropertyChanges { target: downloadButton; Layout.preferredWidth: Theme.Size.none; Layout.preferredHeight: Theme.Size.none; opacity: Theme.Visible.off }
        },

        State {
            when: (status.includes("downloading"))
            name: "downloading"
            PropertyChanges { target: downloadButton; imageSource: Resources.icons.pause; opacity: Theme.Visible.on; Layout.preferredWidth: Theme.Size.icon; Layout.preferredHeight: Theme.Size.icon; onClicked: root.pause() }
        },

        State {
            when: (status === "finished")
            name: "finished"
            PropertyChanges { target: downloadButton; imageSource: Resources.icons.folder; Layout.preferredWidth: Theme.Size.icon; Layout.preferredHeight: Theme.Size.icon; opacity: Theme.Visible.on; onClicked: root.open() }
        }
    ]

    transitions: Transition {
        SequentialAnimation {
            NumberAnimation { properties: "Layout.preferredWidth, Layout.preferredHeight"; duration: Theme.Animation.quick }
            NumberAnimation { property: "opacity"; duration: Theme.Animation.quick }
        }
    }
}
