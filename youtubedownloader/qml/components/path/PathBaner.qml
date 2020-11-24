import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    implicitWidth: mainLayouts.implicitWidth
    implicitHeight: mainLayouts.implicitHeight

    RowLayout {
        id: mainLayouts

        spacing: Theme.Margins.tiny

        Items.YDText {
            Layout.fillWidth: true
            text: "Download to"
        }

        Items.YDImage {
            Layout.preferredWidth: Theme.Size.iconSmall
            Layout.preferredHeight: Theme.Size.iconSmall
            source: Resources.icons.hand
        }
    }
}
