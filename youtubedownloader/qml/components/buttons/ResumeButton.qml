import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Items.YDImageButton {
    id: root

    signal resume()

    onClicked: root.resume()

    imageSource: Resources.icons.redo

    width: Theme.Size.icon
    height: Theme.Size.icon
}
