import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.12

import yd.items 0.1

import "../../items" as Items
import "../../util/regex.js" as Regex
import "../dynamic" as Dynamic

Item {
    id: root

    property var options

    property bool singleLine: true
    property bool firstInitialization: true // NOTE: To do not run the change animation when program start up

    signal addLink(string link)

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    Component.onCompleted: {
        firstInitialization = false
        singleLine = Settings.singleLine
    }

    onSingleLineChanged: Settings.singleLine = root.singleLine

    Component {
        id: singleLineComponent

        Items.YDInput {
            id: link

            placeholderText: qsTr("Enter supported link")
            placeholderTextColor: Theme.Colors.placeholder

            validator: RegularExpressionValidator {
                regularExpression: Regex.URL_REGEX
            }

            focus: true
            rightPadding: Theme.Margins.big * 2 // NOTE: Because of `changeLineButton` position

            onTextEdited: Settings.inputLink = text

            Keys.onEnterPressed: addButton.clicked()
            Keys.onReturnPressed: addButton.clicked()

            Component.onCompleted: {
                text = Settings.inputLink
                if (!root.firstInitialization) {
                    changeSingleLineComponentAnimation.start()
                }
            }

            PropertyAnimation {
                id: changeSingleLineComponentAnimation
                target: link
                from: 100
                to: 40
                property: "implicitHeight"
            }
        }
    }

    Component {
        id: multiLineComponent

        Items.YDScrollableTextArea {
            id: textArea

            placeholderText: qsTr("Enter supported links (remember to separate the links with new line)")
            placeholderTextColor: Theme.Colors.placeholder

            focus: true

            onTextChanged: Settings.inputLink = text

            Component.onCompleted: {
                text = Settings.inputLink
                changeMultiLineComponentAnimation.start()
            }

            PropertyAnimation {
                id: changeMultiLineComponentAnimation
                target: textArea
                from: 40
                to: 100
                property: "implicitHeight"
            }
        }
    }

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Dynamic.Changer {
            id: changer

            Layout.fillWidth: true

            changes: [
                Change {
                    component: singleLineComponent
                    when: root.singleLine
                },

                Change {
                    component: multiLineComponent
                    when: !root.singleLine
                }
            ]
        }

        Items.YDImageButton {
            id: addButton

            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            enabled: root.singleLine ? (changer.item.acceptableInput && !downloadManager.exists(changer.item.text, options)) : changer.item.text

            imageSource: Resources.icons.plus

            onClicked: {
                // BUG: Why it is happening if enabled=False?
                if (!enabled) {
                    return
                }

                if (root.singleLine) {
                    root.addLink(changer.item.text)
                    changer.item.clear()
                } else {
                    for (const url of Regex.extractUrls(changer.item.text)) {
                        root.addLink(url)
                    }
                    changer.item.clear()
                }

                Settings.inputLink = Theme.String.empty
            }
        }
    }

    Items.YDPureImageButton {
        id: changeLineButton

        parent: changer.item

        anchors {
            right: parent.right
            rightMargin: Theme.Margins.small
            verticalCenter: parent.verticalCenter
        }

        width: Theme.Size.iconSmall
        height: Theme.Size.iconSmall

        imageSource: Resources.icons.arrowDown

        onClicked: root.singleLine = !root.singleLine
    }

    states: [
        State {
            when: root.singleLine
            PropertyChanges {
                target: changeLineButton
                rotation: 0
            }
        },

        State {
            when: !root.singleLine
            PropertyChanges {
                target: changeLineButton
                rotation: 180
            }
        }
    ]

    transitions: [
        Transition {
            RotationAnimation { duration: Theme.Animation.quick }
        }
    ]
}
