import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Rectangle {
    id: root

    property alias existsPath: existsInfo.text

    radius: Theme.Margins.tiny
    color: Theme.Colors.shadowError

    ColumnLayout {
        id: mainLayout
        anchors.centerIn: parent
        spacing: Theme.Margins.tiny

        Items.YDText {
            id: textItem
            Layout.fillWidth: true
            font.bold: true
            text: qsTr("Already exists")
        }

        Items.YDText {
            id: existsInfo
            Layout.fillWidth: true
        }
    }
}
