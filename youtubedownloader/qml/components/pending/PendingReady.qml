import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as Link
import "../format" as Format
import ".." as Components

Item {
    id: root

    property string url
    property string destinationFile

    property var downloadData
    property var downloadOptions

    signal remove()

    signal changeFormat(string format)
    signal changeOutputPath(string path)

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

            link: url

            Layout.fillWidth: true
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
