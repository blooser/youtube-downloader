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

   property int buttonsPolicy: buttons.OPEN | buttons.PAUSE_RESUME | buttons.DELETE

   readonly property var buttons: {
       "OPEN": 1,
       "PAUSE_RESUME": 2,
       "DELETE": 4
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

        Buttons.PauseResumeButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttons.PAUSE_RESUME

            onPause: root.pause()
            onResume: root.resume()
        }

        Buttons.DeleteButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            visible: root.buttonsPolicy & buttonsbuttons.DELETE

            onRemove: root.remove()
        }
    }
}
