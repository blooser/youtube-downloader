import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Items.YDImageButton {
    signal open()

    onClicked: root.open()

    imageSource: Resources.icons.eye

    width: Theme.Size.icon
    height: Theme.Size.icon
}
