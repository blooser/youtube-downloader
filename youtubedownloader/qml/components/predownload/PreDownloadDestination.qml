import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property string destination

    signal changeDestination(string newDestination)

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Items.YDPureImageButton {
            Layout.preferredWidth: 24
            Layout.preferredHeight: 24
            imageSource: Resources.icons.folder

            onClicked: dialogManager.open_dialog("SelectDirectoryDialog", {"folder": root.destination}, function(path) {
                let cleanPath = Paths.cleanPath(path)
                if (cleanPath !== root.destination) {
                    root.changeDestination(cleanPath)
                }
            })
        }

        Items.YDText {
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignLeft
            font.pixelSize: Theme.FontSize.micro
            text: root.destination
        }
    }
}
