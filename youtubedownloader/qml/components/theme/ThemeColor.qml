import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property string text
    property color color

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDText {
            Layout.fillWidth: true

            text: root.text
        }

        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 100
            Layout.preferredHeight: 100

            color: root.color

            anchors.margins: Theme.Margins.tiny

            border {
                color: Theme.Colors.base
                width: Theme.Size.border
            }
        }
    }
}

