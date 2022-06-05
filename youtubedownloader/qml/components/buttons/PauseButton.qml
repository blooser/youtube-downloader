import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Items.YDImageButton {
    id: root

    signal pause()

    onClicked: root.pause()

    imageSource: Resources.icons.pause

    width: Theme.Size.icon
    height: Theme.Size.icon
}
