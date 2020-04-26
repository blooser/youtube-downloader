import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items

Popup {
    id: root

    implicitWidth: 100

    modal: true
    focus: true

    padding: Theme.Margins.tiny

    contentItem: ListView {
        id: formats

        boundsBehavior: Flickable.StopAtBounds
        clip: true
        implicitHeight: contentHeight
        model: Settings.fileFormats

        delegate: FormatItemDelegate {
            width: formats.width
            text: modelData
        }

        ScrollIndicator.vertical: ScrollIndicator { }
    }

    background: Rectangle {
        border.color: Theme.Colors.third
        color: Theme.Colors.base
        radius: Theme.Margins.tiny
    }
}
