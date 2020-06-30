import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property alias error: error.text

    signal remove()

    implicitWidth: mainLayout.minimumWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            margins: Theme.Margins.normal
        }

        spacing: Theme.Margins.tiny

        Items.YDImage {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            source: Resources.icons.dizzy
        }

        Items.YDText {
            id: error
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
       }

        Items.YDImageButton {
            Layout.alignment: Qt.AlignRight
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            width: Theme.Size.icon
            height: Theme.Size.icon

            imageSource: Resources.icons.delete

            onClicked: root.remove()
        }
    }
}
