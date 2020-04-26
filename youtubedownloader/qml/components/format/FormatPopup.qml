import QtQuick 2.14
import QtQuick.Controls 2.14

import "../../items" as Items

Popup {
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
        model: Settings.fileFormats

        delegate: FormatItemDelegate {
            width: formats.width
            text: modelData
            enabled: !downloadManager.exists(link, optionsWithNewFormat(modelData))
            onClicked: {
                root.formatSelected(modelData)
                root.close()
            }
        }

        ScrollIndicator.vertical: ScrollIndicator { }
    }

    background: Rectangle {
        border.color: Theme.Colors.third
        color: Theme.Colors.base
        radius: Theme.Margins.tiny
    }
}
