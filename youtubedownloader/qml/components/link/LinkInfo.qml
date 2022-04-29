import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property var info

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.normal

        Items.YDThumbnail {
            source: info.thumbnail

            Layout.preferredWidth: 86
            Layout.preferredHeight: 86
        }

        ColumnLayout {
            spacing: Theme.Margins.tiny

            Items.YDLink {
                Layout.fillWidth: true

                link: info.url
                text: info.title

                font.pixelSize: Theme.FontSize.normal
                horizontalAlignment: Text.AlignLeft
            }

            RowLayout {
                spacing: Theme.Margins.small

                Items.YDLink {
                    text: info.uploader
                    link: info.uploader_url

                    visible: (text !== Theme.String.empty)
                    horizontalAlignment: Text.AlignLeft
                }

                Components.IconText {
                    text: info.duration
                    iconSource: Resources.icons.time
                }

                Components.IconText {
                    text: info.view_count
                    iconSource: Resources.icons.eye
                }

                Components.IconText {
                    text: info.upload_date
                    iconSource: Resources.icons.calendar
                }
            }
        }
    }
}
