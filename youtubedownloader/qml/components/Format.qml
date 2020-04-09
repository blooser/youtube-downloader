import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.12

import "../items" as Items

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ButtonGroup {
        id: buttonGroup
        buttons: mainLayout.children
        onClicked: Settings.selectedType = button.text
    }

    RowLayout {
        id: mainLayout

        spacing: Theme.Margins.tiny

        Items.YDButton {
            checked: (text === Settings.selectedType)
            checkable: true
            text: qsTr("webm")
        }

        Items.YDButton {
           checked: (text === Settings.selectedType)
           checkable: true
           text: qsTr("mp4")
        }

        Items.YDButton {
            checked: (text === Settings.selectedType)
            checkable: true
            text: qsTr("mp3")
        }
    }
}
