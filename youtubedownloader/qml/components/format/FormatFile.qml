import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items

Item {
    id: root

    signal fileFormatChanged(string fileFormat)

    readonly property var parentByFileFormat: {
        "video": videos,
        "audio": audios,
        "": undefined
    }

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    ButtonGroup {
        id: buttonGroup
        onClicked: root.fileFormatChanged(button.text)
    }

    RowLayout {
        id: mainLayout

        spacing: Theme.Margins.tiny

        GroupBox {
            Layout.fillWidth: true

            RowLayout {
                id: videos
            }
        }

        GroupBox {
            Layout.fillWidth: true

            RowLayout {
                id: audios
            }
        }
    }

    Component {
        id: fileFormatButton

        Items.YDButton {
            checked: (text === Settings.fileFormat)
            checkable: true
        }
    }

    Component.onCompleted: {
        for (let fileFormat of Settings.fileFormats) {
            buttonGroup.buttons.push(fileFormatButton.createObject(parentByFileFormat[Paths.getFileType(fileFormat)], {"text": fileFormat}))
        }
    }
}
