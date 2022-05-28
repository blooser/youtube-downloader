import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Items.YDImageButton {
    signal remove()

    onClicked: root.remove()

    width: Theme.Size.icon
    height: Theme.Size.icon

    imageSource: Resources.icons.delete
}
