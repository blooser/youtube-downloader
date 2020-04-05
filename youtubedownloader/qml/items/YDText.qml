import QtQuick 2.14

Text {
    id: root

    color: Theme.Colors.text

    font {
        pixelSize: Theme.FontSize.small
    }

    elide: Text.ElideRight

    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
}
