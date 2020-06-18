import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items
import ".." as Components

TextField {
    id: root

    color: Theme.Colors.text
    placeholderText: qsTr("Enter thumbnail's filename")

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 40
        color: Theme.Colors.shadowBlack

        border {
            width: Theme.Size.border
            color: root.activeFocus ? Theme.Colors.highlight : Theme.Colors.base
        }
    }
}
