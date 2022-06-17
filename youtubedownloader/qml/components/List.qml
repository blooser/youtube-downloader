import QtQuick 2.14
import QtQuick.Layouts 1.14

import "../items" as Items

Item {
    id: root

    readonly property int count: list.count

    property bool hide: false
    property string label: "unknown"

    property var model: null
    property Component delegate: null

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + list.contentHeight

    visible: list.count

    onHideChanged: {
        root.state = root.hide ? "hide" : ""
    }

    ColumnLayout {
        id: mainLayout

        anchors.fill: root

        spacing: Theme.Margins.tiny

        DownloadsLabel {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            text: root.label
            counter: list.count

            MouseArea {
                anchors.fill: parent
                onClicked: root.hide = !root.hide
            }
        }

        Items.YDList {
            id: list

            Layout.fillWidth: true
            Layout.fillHeight: true

            boundsBehavior: Flickable.StopAtBounds

            spacing: Theme.Margins.tiny
            clip: true

            model: root.model

            delegate: root.delegate
        }
    }

    states: [
        State {
            name: "hide"

            PropertyChanges {
                target: list

                opacity: 0
                height: 0
            }

            PropertyChanges {
                target: root

                implicitHeight: mainLayout.implicitHeight
            }
        }
    ]

    transitions: [
        Transition {
            from: "*"; to: "hide"

           SequentialAnimation {
                OpacityAnimator { duration: Theme.Animation.quick }
                ParallelAnimation {
                    PropertyAnimation { property: "implicitHeight"; duration: Theme.Animation.quick }
                    PropertyAnimation { property: "height"; duration: Theme.Animation.quick }
                }
           }
        },

        Transition {
            from: "hide"; to: "*"

           SequentialAnimation {
                ParallelAnimation {
                    PropertyAnimation { property: "implicitHeight"; duration: Theme.Animation.quick }
                    PropertyAnimation { property: "height"; duration: Theme.Animation.quick }
                }
                OpacityAnimator { duration: Theme.Animation.quick }
           }
        }
    ]
}
