import QtQuick 2.14

import QtQuick.Layouts 1.14

import ".." as Components

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight + downloadItems.contentHeight

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent

        spacing: Theme.Margins.tiny

        Components.DownloadsLabel {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            opacity: downloadItems.count
            text: qsTr("Downloaded")
            counter: downloadItems.count

            Behavior on opacity {
                NumberAnimation {
                    duration: Theme.Animation.quick
                }
            }
        }

        ListView {
            id: downloadItems

            Layout.fillWidth: true
            Layout.fillHeight: true

            boundsBehavior: Flickable.StopAtBounds
            clip: true
            spacing: Theme.Margins.tiny
            model: downloadManager.downloadModel

            add: Transition {
                OpacityAnimator { from: Theme.Visible.off; to: Theme.Visible.on; duration: Theme.Animation.quick }
            }

            delegate: DownloadItem {
                width: downloadItems.width

                downloadStatus: status
                downloadInfo: info
                downloadOptions: options
                downloadProgress: progress
            }
        }
    }
}
