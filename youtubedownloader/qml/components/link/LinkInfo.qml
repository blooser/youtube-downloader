import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property alias link: title.link
    property alias titleText: title.text
    property alias uploaderText: uploader.text
    property alias uploaderLink: uploader.link
    property alias durationText: duration.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDLink {
            id: title

            Layout.fillWidth: true
            font.pixelSize: Theme.FontSize.normal
            horizontalAlignment: Text.AlignLeft
        }

        RowLayout {
            spacing: Theme.Margins.small

            Items.YDLink {
                id: uploader

                horizontalAlignment: Text.AlignLeft
            }

            Components.IconText {
                id: duration

                iconSource: Resources.icons.time
            }
        }
    }
}
