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

        Items.YDGroupBox {
            Layout.fillWidth: true
            labelText: qsTr("Video + Audio")

            RowLayout {
                id: videos
            }
        }

        Items.YDGroupBox {
            Layout.fillWidth: true
            labelText: qsTr("Audio")

            RowLayout {
                id: audios
            }
        }
    }

    Component {
        id: fileFormatButton

        Items.YDButtonWithHelp {
            checked: (text === Settings.fileFormat)
            checkable: true
            onHelp: dialogManager.open_dialog("FileFormatsDialog", {"format": text}, null)
        }
    }

    Component.onCompleted: {
        let index = 0
        for (let fileFormat of Settings.fileFormats) {
            buttonGroup.buttons.push(fileFormatButton.createObject(parentByFileFormat[Paths.getFileType(fileFormat)], {"text": fileFormat}))
        }
    }
}
