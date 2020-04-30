import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../../util/regex.js" as Regex

Item {
    id: root

    property var options

    signal addLink(string link)

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Items.YDInput {
            id: link

            Layout.fillWidth: true
            placeholderText: qsTr("Enter youtube link")
            placeholderTextColor: Theme.Colors.placeholder

            onTextEdited: Settings.inputLink = text

            validator: RegularExpressionValidator {
                regularExpression: Regex.YOUTUBE_LINK_REGEX
            }

            Keys.onEnterPressed: addButton.clicked()
            Keys.onReturnPressed: addButton.clicked()

            Component.onCompleted: {
                text = Settings.inputLink
            }
        }

        Items.YDImageButton {
            id: addButton

            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            enabled: (link.acceptableInput && !downloadManager.exists(link.text, options))

            imageSource: Resources.icons.plus

            onClicked: {
                // BUG: Why it is happening if enabled=False?
                if (!enabled) {
                    return
                }

                root.addLink(link.text)
                link.clear()
                Settings.inputLink = Theme.String.empty
            }
        }
    }
}
