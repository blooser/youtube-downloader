import QtQuick 2.14
import QtQuick.Layouts 1.15

Item {
    id: root

    property string text: ""

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Separator {

        }

        TileText {
            Layout.alignment: Qt.AlignHCenter

            text: root.text
            font.pixelSize: 10
        }

        Separator {

        }
    }
}
