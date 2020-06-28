import QtQuick 2.14

Rectangle {
    id: root

    implicitWidth: historyItems.implicitWidth
    implicitHeight: historyItems.implicitHeight

    color: Theme.Colors.second

    HistoryItems {
        id: historyItems

        anchors {
            fill: parent
            margins: Theme.Margins.big
        }
    }
}
