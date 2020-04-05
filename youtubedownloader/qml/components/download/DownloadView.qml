import QtQuick 2.14
import QtQuick.Layouts 1.12

Rectangle {
    id: root

    color: Theme.Colors.blank
    radius: Theme.Margins.tiny

    border {
        width: Theme.Size.border
        color: Theme.Colors.second
    }

    implicitWidth: downloadItems.implicitWidth
    implicitHeight: downloadItems.implicitHeight

    DownloadItems {
        id: downloadItems

        anchors {
            fill: parent
            margins: Theme.Margins.tiny
        }
    }
}
