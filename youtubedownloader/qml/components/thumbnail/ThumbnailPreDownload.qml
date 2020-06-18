import QtQuick 2.14

import "../../items" as Items

Item {
    id: root

    signal close()
    signal download()

    MouseArea {
        anchors.fill: parent
        onClicked: root.close()
    }

    Items.YDButton {
        text: qsTr("Download")

        anchors {
            horizontalCenter: root.horizontalCenter
            bottom: root.bottom
            bottomMargin: Theme.Margins.big
        }

        onClicked: root.download()
    }
}
