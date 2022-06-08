import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../items" as Items

Item {
    id: root

    signal download()

    property bool ready: false

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Separator {

        }

        // TODO: Make the separators connect if button is not visible
        Items.YDButton {
            text: qsTr("Download")
            icon.source: Resources.icons.download

            onClicked: root.download()

            opacity: root.ready
            enabled: root.ready

            Behavior on opacity {
                PropertyAnimation { duration: Theme.Animation.quick }
            }
        }

        Separator {

        }
    }
}
