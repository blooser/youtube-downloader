import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property alias thumbnailSource: thumbnail.source
    property alias link: title.link
    property alias titleText: title.text
    property alias uploaderText: uploader.text
    property alias uploaderLink: uploader.link
    property alias durationText: duration.text
    property alias viewCount: viewCount.text
    property alias uploadDate: uploadDate.text

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.normal

        Items.YDThumbnail {
            id: thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86
        }

        ColumnLayout {
            spacing: Theme.Margins.tiny

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

                Components.IconText {
                    id: viewCount

                    iconSource: Resources.icons.eye
                }

                Components.IconText {
                    id: uploadDate

                    iconSource: Resources.icons.calendar
                }
            }
        }
    }
}
