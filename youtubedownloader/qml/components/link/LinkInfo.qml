import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

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

            font.pixelSize: Theme.FontSize.normal
            horizontalAlignment: Text.AlignLeft
        }

        RowLayout {
            spacing: Theme.Margins.tiny

            Items.YDLink {
                id: uploader

                horizontalAlignment: Text.AlignLeft
            }

            Items.YDText {
                id: duration

                horizontalAlignment: Text.AlignLeft
            }
        }
    }
}
