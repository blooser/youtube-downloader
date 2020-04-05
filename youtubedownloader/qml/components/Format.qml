import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.12

import "../items" as Items

Item {
    id: root

    property string format: "webm"

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ButtonGroup {
        id: buttonGroup
        buttons: mainLayout.children
    }

    RowLayout {
        id: mainLayout

        spacing: Theme.Margins.tiny

        Items.YDButton {
            checked: true
            checkable: true
            text: qsTr("webm")

            onClicked: format = text
        }

        Items.YDButton {
           checkable: true
           text: qsTr("mp4")

           onClicked: format = text
        }

        Items.YDButton {
            checkable: true
            text: qsTr("mp3")

            onClicked: format = text
        }
    }
}
