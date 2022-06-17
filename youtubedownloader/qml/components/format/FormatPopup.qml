import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items

Items.YDPopup {
    id: root

    property var options

    signal formatSelected(string format)

    modal: true
    focus: true

    padding: Theme.Margins.tiny

    implicitWidth: 100

    contentItem: ListView {
        id: formats

        boundsBehavior: Flickable.StopAtBounds
        clip: true
        implicitHeight: contentHeight
        model: FormatFileDescriptionModel {}

        delegate: FormatItemDelegate {
            width: formats.width

            text: format

            enabled: root.options.format !== format

            onClicked: {
                root.formatSelected(format)
                root.close()
            }
        }

        ScrollIndicator.vertical: ScrollIndicator { }
    }
}
