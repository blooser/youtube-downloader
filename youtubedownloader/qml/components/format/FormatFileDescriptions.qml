import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property var setFormat: function (format) {
        for (let i=0; i<fileFormatsRepeater.count; ++i) {
            if (fileFormatsRepeater.itemAt(i).text.includes(format)) {
                tabBar.setCurrentIndex(i)
                return
            }
        }
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDTabBar {
            id: tabBar

            Layout.fillWidth: true

            Repeater {
                id: fileFormatsRepeater

                model: FormatFileDescriptionModel {}

                Items.YDTabButton {
                    text: format
                }
            }
        }

        SwipeView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            clip: true
            currentIndex: tabBar.currentIndex

            Repeater {
                model: FormatFileDescriptionModel {}

                FormatFileDescription {
                    mediaType: type
                    formatDescription: description
                    readMoreLink: readMore
                }
            }
        }
    }
}
