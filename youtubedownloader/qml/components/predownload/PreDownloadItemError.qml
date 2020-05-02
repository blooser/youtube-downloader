import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property alias error: error.text

    Row {
        anchors.centerIn: parent
        spacing: Theme.Margins.tiny

        Items.YDImage {
            width: Theme.Size.icon
            height: Theme.Size.icon
            source: Resources.icons.dizzy
        }

        Items.YDText {
            id: error
            horizontalAlignment: Qt.AlignLeft
        }
    }
}
