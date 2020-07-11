import QtQuick 2.14

import "../items" as Items

Items.YDInput {
    id: root

    property bool empty: (text === Theme.String.empty)

    icon: !root.empty
    iconSource: Resources.icons.close

    onIconClicked: {
        clear()
        focus = true
    }
}
