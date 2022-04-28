import QtQuick 2.15
import QtQuick.Layouts 1.15

import "../../items" as Items
import "../dynamic" as Dynamic
import ".." as Components


Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + pending.contentHeight


    ColumnLayout {
        id: mainLayout
        spacing: Theme.Margins.tiny

        anchors.fill: parent

        Items.YDButton {
            Layout.alignment: Qt.AlignHCenter

            icon.source: Resources.icons.download

            text: qsTr("Download")

            onClicked: console.log("Downloading!")
        }

        Components.DownloadsLabel {
            Layout.fillWidth: true

            text: qsTr("Pending")
            counter: pending.count

            Behavior on opacity {
                NumberAnimation {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: pending

            Layout.fillWidth: true
            Layout.fillHeight: true

            boundsBehavior: Flickable.StopAtBounds
            clip: true
            spacing: Theme.Margins.tiny
            model: pendingManager.model

            remove: Transition {
                OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
            }

            removeDisplaced: Transition {
                NumberAnimation { property: "y"; duration: Theme.Animation.quick }
            }

            delegate: PendingItem {
                width: pending.width

                status: status
            }
        }
    }
}
