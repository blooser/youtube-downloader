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

            onOpen: root.open()
        }

        Buttons.PauseResumeButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            onPause: root.pause()
            onResume: root.resume()
        }

        Buttons.DeleteButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon
            Layout.alignment: Qt.AlignRight

            onRemove: root.remove()
        }
    }
}
