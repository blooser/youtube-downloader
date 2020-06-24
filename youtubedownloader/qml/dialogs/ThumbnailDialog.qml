import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

import "../components/thumbnail" as Thumbnail
import "../items" as Items
import "../util/numbers.js" as Numbers

YDDialog {
    id: root

    property string url

    dialog: "ThumbnailDialog"

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    header: null
    footer: null
    standardButtons: Dialog.NoButton
    contentItem: Thumbnail.Thumbnail {
        source: root.url
        onClose: root.close()

        states: State {
            when: (implicitWidth >= Screen.desktopAvailableWidth || implicitHeight >= Screen.desktopAvailableHeight)
            PropertyChanges {
                target: root
                implicitWidth: root.implicitWidth - Numbers.WINDOW_MARGIN
                implicitHeight: root.implicitHeight - Numbers.WINDOW_MARGIN
            }
        }
    }
}
