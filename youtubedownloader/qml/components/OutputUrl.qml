import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    property string url

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.big

        Items.YDText {
            Layout.fillWidth: true
            style: Text.Outline
            styleColor: Theme.Colors.textStyle
            text: root.url
        }

        Items.YDImageButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            imageSource: Resources.icons.eye

            onClicked: Qt.openUrlExternally(root.url)
        }
    }
}
