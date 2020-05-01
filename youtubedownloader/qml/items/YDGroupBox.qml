import QtQuick 2.14
import QtQuick.Controls 2.14


GroupBox {
    id: root

    property alias labelText: labelText.text

    background: Rectangle {
        y: root.topPadding - root.bottomPadding
        width: parent.width
        height: parent.height - root.topPadding + root.bottomPadding
        color: Theme.Colors.blank
        border.color: Theme.Colors.third
        radius: Theme.Margins.tiny


        Rectangle {
            anchors {
                top: parent.top
                topMargin: -Theme.Margins.tiny
                horizontalCenter: parent.horizontalCenter
            }

            implicitWidth: labelText.implicitWidth
            implicitHeight: labelText.implicitHeight

            visible: (labelText.text.length > 0)

            color: Theme.Colors.third
            radius: Theme.Margins.tiny

            YDText {
                id: labelText
                padding: Theme.Size.border
                font.pixelSize: Theme.FontSize.groupBoxLabel

                style: Text.Raised
                styleColor: Theme.Colors.textStyle
            }
        }
    }
}
