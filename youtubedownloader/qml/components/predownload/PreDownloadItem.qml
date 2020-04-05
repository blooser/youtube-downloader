import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import ".." as Components

Rectangle {
    id: root

    property alias thumbnailUrl: thumbnail.source
    property alias linkTitle: link.title
    property alias linkUploader: link.uploader
    property alias selectedFormat: selectedFormat.format

    signal remove()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: Theme.Colors.second
    radius: Theme.Margins.tiny

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

        spacing: Theme.Margins.big

        Items.YDImage {
            id: thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86
        }

        Components.Link {
            id: link

            Layout.fillWidth: true
        }

        Components.SelectedFormat {
            id: selectedFormat

            Layout.preferredWidth: 50
            Layout.preferredHeight: 35
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }
}
