import QtQuick 2.14

import "../../items" as Items
import ".." as Components
import "../../util/numbers.js" as Numbers

Item {
    id: root

    property alias to: progress.to
    property alias value: progress.value

    property alias outputUrl: outputUrl.url

    Components.OutputUrl {
        id: outputUrl

        anchors {
            left: progress.left
            right: progress.right
            bottom: progress.top
            bottomMargin: Theme.Margins.small
        }

        opacity: (url !== "" && progress.value === progress.to && progress.to !== 0)

        Behavior on opacity {
            NumberAnimation { duration: Theme.Animation.quick }
        }
    }

    Items.YDProgressBar {
        id: progress

        implicitHeight: Theme.Margins.big

        anchors {
            left: root.left
            right: root.right
            bottom: root.bottom
            margins: Theme.Margins.big
        }

        Items.YDText {
            z: parent.z + 1
            anchors.centerIn: parent
            style: Text.Outline
            styleColor: Theme.Colors.textStyle
            text: qsTr(Numbers.progress(progress.value, progress.to))
        }
    }
}
