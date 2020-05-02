import QtQuick 2.14

YDText {
    id: root

    signal clicked()

    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
