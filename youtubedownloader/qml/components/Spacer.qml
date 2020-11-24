import QtQuick 2.14
import QtQuick.Layouts 1.14

Item {
    property int orientation: Qt.Horizontal

    Layout.fillWidth: (orientation === Qt.Horizontal)
    Layout.fillHeight: (orientation === Qt.Vertical)
}
