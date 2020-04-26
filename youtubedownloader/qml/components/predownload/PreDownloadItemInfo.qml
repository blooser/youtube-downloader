import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as Link
import "../format" as Format
import ".." as Components

Item {
    id: root

    property alias thumbnailUrl: thumbnail.source
    property alias link: link.link
    property alias linkTitle: link.titleText
    property alias linkUploader: link.uploaderText
    property alias linkUploaderLink: link.uploaderLink
    property alias linkDuration: link.durationText
    property alias selectedFormat: selectedFormat.text

    property var downloadOptions

    signal remove()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

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

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true
        }

        Format.FormatSelected {
            id: selectedFormat

            Layout.preferredWidth: 65

            downloadOptions: root.downloadOptions
            link: root.link
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }
}
