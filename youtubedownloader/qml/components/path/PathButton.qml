import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import ".." as Components

Items.YDButton {
    id: root

    contentItem: Item {
        Items.YDText {
            text: Settings.outputPath
            anchors.centerIn: parent

            PathBaner {
                anchors {
                    right: parent.left
                    rightMargin: Theme.Margins.tiny
                }
            }
        }
    }
}
