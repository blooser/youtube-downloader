import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as  Link
import ".." as Components

Items.YDProgressBar {
    id: root

    property alias statusText: status.text
    property alias thumbnailSrc: thumbnail.source
    property alias titleText: link.titleText
    property alias uploaderText: link.uploaderText
    property alias linkDuration: link.durationText

    property alias selectedFormat: selectedFormat.format

    signal remove()
    signal open()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        z: root.z + 1
        spacing: Theme.Margins.normal

        anchors {
            fill: parent
            leftMargin: Theme.Margins.tiny
            rightMargin: Theme.Margins.tiny
        }

        Items.YDImage {
            id: thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86
        }

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true
        }

        Items.YDText {
            id: status
        }

        Components.SelectedFormat {
            id: selectedFormat

            Layout.preferredWidth: 50
            Layout.preferredHeight: 35
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            imageSource: Resources.icons.folder

            onClicked: root.open()
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }
}
