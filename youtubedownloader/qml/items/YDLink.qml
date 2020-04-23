import QtQuick 2.14

YDText {
    property string link

    MouseArea {
        anchors.fill: parent
        onClicked: Qt.openUrlExternally(link)
    }
}
