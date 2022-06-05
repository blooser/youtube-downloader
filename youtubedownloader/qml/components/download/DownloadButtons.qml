import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../buttons" as Buttons

Item {
   id: root

   signal open()
   signal resume()
   signal pause()
   signal remove()

   property int buttonsPolicy: buttons.OPEN | buttons.PAUSE | buttons.RESUME | buttons.DELETE

   readonly property var buttons: {
       "OPEN": 1,
       "PAUSE": 2,
       "RESUME": 4,
       "DELETE": 8
   }

   implicitWidth: mainLayout.implicitWidth
   implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        Buttons.OpenButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttons.OPEN

            onOpen: root.open()
        }

        Buttons.PauseButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttons.PAUSE

            onPause: root.pause()
        }

        Buttons.ResumeButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttons.RESUME

            onResume: root.resume()
        }

        Buttons.DeleteButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttons.DELETE

            onRemove: root.remove()
        }
    }
}
