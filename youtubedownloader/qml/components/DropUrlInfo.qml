import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtGraphicalEffects 1.14

import "../items" as Items

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDText {
            id: dropTextInfo

            Layout.fillWidth: true

            text: qsTr("Drop your mouse to add new download")

            font {
                pixelSize: Theme.FontSize.big
                bold: true
            }

            style: Text.Raised
            styleColor: Theme.Colors.textStyle
        }

        Items.YDImage {
            id: animatedArrow

            Layout.preferredWidth: 84
            Layout.preferredHeight: 84
            Layout.alignment: Qt.AlignHCenter

            readonly property real startY: y

            source: Resources.icons.arrowDown

            ColorOverlay {
                anchors.fill: parent
                source: parent
                color: Theme.Colors.third
                visible: (parent.status === Image.Ready)
            }

            SequentialAnimation on y {
                loops: Animation.Infinite
                PropertyAnimation { to: animatedArrow.startY + Theme.Margins.big * 2.5 ; duration: Theme.Animation.medium }
                PropertyAnimation { to: animatedArrow.startY; duration: Theme.Animation.quick }
            }
        }
    }
}
