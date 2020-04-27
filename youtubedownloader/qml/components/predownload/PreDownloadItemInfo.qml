import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as Link
import "../format" as Format
import ".." as Components

Item {
    id: root

    property string link

    property var downloadData
    property var downloadOptions

    signal remove()
    signal changeFormat(string format)

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

        Link.LinkInfo {
            id: link

            Layout.fillWidth: true

            thumbnailSource: downloadData.thumbnail
            link: root.link
            titleText: downloadData.title
            uploaderText: downloadData.uploader
            uploaderLink: downloadData.uploaderUrl
            durationText: downloadData.duration
        }

        Format.FormatSelected {
            id: selectedFormat

            Layout.preferredWidth: 65

            link: root.link
            downloadOptions: root.downloadOptions

            onChangeFormat: root.changeFormat(format)
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }
}
