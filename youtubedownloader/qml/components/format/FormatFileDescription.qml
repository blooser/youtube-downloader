import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property alias mediaType: mediaType.text
    property alias formatDescription: description.text
    property alias readMoreLink: readMore.link

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDText {
            id: mediaType

            Layout.fillWidth: true

            font.bold: true
        }

        Items.YDText {
            id: description

            Layout.fillWidth: true
            Layout.fillHeight: true

            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WordWrap
        }

        Items.YDLink {
            id: readMore

            Layout.fillWidth: true

            horizontalAlignment: Text.AlignRight
            text: "Read More"
        }
    }
}
