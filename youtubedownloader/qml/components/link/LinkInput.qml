import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Item {
    id: root

    signal addLink(string link)

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDInput {
            id: link

            Layout.fillWidth: true
            placeholderText: qsTr("Enter your link")
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.plus

            onClicked: {
                root.addLink(link.text)
                link.clear()
            }
        }
    }
}
