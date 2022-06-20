import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: root
        spacing: Theme.Margins.big


        Items.YDImage {
            id: animatedArrow

            Layout.preferredWidth: 84
            Layout.preferredHeight: 84
            Layout.alignment: Qt.AlignHCenter

            readonly property real startY: y

            source: Resources.icons.arrowDown

            SequentialAnimation on y {
                loops: Animation.Infinite
                PropertyAnimation { to: animatedArrow.startY + Theme.Margins.big * 2.5 ; duration: Theme.Animation.medium }
                PropertyAnimation { to: animatedArrow.startY; duration: Theme.Animation.quick }
            }
        }
    }
}
