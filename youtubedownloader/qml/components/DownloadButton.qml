import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../items" as Items

Item {
    id: root

    signal download()

    property bool ready: false

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent

        Separator {

        }

        // TODO: Make the separators connect if button is not visible
        Items.YDButton {
            id: downloadButton

            text: qsTr("Download")
            icon.source: Resources.icons.download

            onClicked: root.download()

            enabled: root.ready

            onEnabledChanged: downloadButton.state = !enabled ? "hide" : ""

            Behavior on opacity {
                PropertyAnimation { duration: Theme.Animation.quick }
            }

            states: State {
                name: "hide"

                PropertyChanges {
                    target: downloadButton

                    opacity: 0
                    implicitWidth: 0
                }
            }

            transitions: [
                Transition {
                    from: "*"; to: "hide"

                    SequentialAnimation {
                        OpacityAnimator { duration: Theme.Animation.quick }
                        PropertyAnimation { property: "implicitWidth"; duration: Theme.Animation.quick }
                    }
                },

                Transition {
                    from: "hide"; to: "*"

                    SequentialAnimation {
                        PropertyAnimation { property: "implicitWidth"; duration: Theme.Animation.quick }
                        OpacityAnimator { duration: Theme.Animation.quick }
                    }
                }
            ]
        }

        Separator {

        }
    }
}
