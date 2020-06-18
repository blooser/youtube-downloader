import QtQuick 2.14

import "../../items" as Items

Item {
    id: root

    signal download()

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
