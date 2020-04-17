import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Item {
    id: root

    signal open()

   implicitWidth: mainLayout.implicitWidth
   implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.folder

            onClicked: root.open()
        }
    }
}
