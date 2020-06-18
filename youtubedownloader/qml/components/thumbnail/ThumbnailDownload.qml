import QtQuick 2.14

import "../../items" as Items

Item {
    id: root

    property alias to: progress.to
    property alias value: progress.value

    Items.YDProgressBar {
        id: progress

        implicitHeight: Theme.Margins.big

        anchors {
            left: root.left
            right: root.right
            bottom: root.bottom
            margins: Theme.Margins.big
        }
    }
}
