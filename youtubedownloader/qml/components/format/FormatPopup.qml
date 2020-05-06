import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items

Items.YDPopup {
    id: root

    property var downloadOptions
    property string link

    property var optionsWithNewFormat: function (format) {
        return {
            "output_path": downloadOptions.outputPath,
            "file_format": format
        }
    }

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
            enabled: !downloadManager.exists(link, optionsWithNewFormat(format))
            onClicked: {
                root.formatSelected(format)
                root.close()
            }
        }

        ScrollIndicator.vertical: ScrollIndicator { }
    }
}
