import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Items.YDImageButton {
    signal pause()
    signal resume()

    property bool isActive: true

    width: Theme.Size.icon
    height: Theme.Size.icon

    imageSource: isActive ? Resources.icons.pause
                          : Resources.icons.redo

    onClicked: {
        if (isActive) {
            root.pause()
        } else {
            root.resume()
        }

        isActive = !isActive
    }
}
