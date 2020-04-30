import QtQuick 2.14
import QtQuick.Controls 2.14

Image {
    id: root

    asynchronous: true
    fillMode: Image.PreserveAspectFit

    YDBusyIndicator {
        anchors.fill: parent
        running: (root.status === Image.Loading)
        visible: running
    }
}
