import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import "../buttons" as Buttons
import "../link" as Link
import ".." as Components

import youtubedownloader.component.changer


Rectangle {
    id: root

    property var downloadStatus
    property var downloadInfo
    property var downloadOptions

    signal remove()
    signal open()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: Theme.Colors.success

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

            text: "Finished"
        }

        Components.Spacer {

        }

        Components.TileText {
            Layout.preferredWidth: 65

            text: root.downloadOptions.format
        }

        Buttons.OpenButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            onOpen: root.open()
        }

        Buttons.DeleteButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            onRemove: root.remove()
        }
    }
}

