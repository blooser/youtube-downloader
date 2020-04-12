import QtQuick 2.14
import QtQuick.Controls 2.14

import Qt.labs.settings 1.1

import "predownload" as PreDownload
import "download" as Download
import "../items" as Items

Item {
    id: root

    implicitWidth: splitView.implicitWidth
    implicitHeight: splitView.implicitHeight

    Component.onCompleted: splitView.restoreState(splitViewSettings.splitView)
    Component.onDestruction: splitViewSettings.splitView = splitView.saveState()

    Settings {
        id: splitViewSettings
        property var splitView
    }

    Items.YDSplitView {
        id: splitView

        anchors.fill: parent

        orientation: Qt.Vertical

        PreDownload.PreDownloadView {
            SplitView.fillWidth: true
            SplitView.preferredHeight: root.height/2
        }

        Download.DownloadView {
            SplitView.fillWidth: true
            SplitView.preferredHeight: root.height/2
        }
    }

    state: "empty"

    states: [
        State {
            name: "empty"
            when: (predownloadModel.size === Theme.Capacity.empty && downloadModel.size === Theme.Capacity.empty)
            PropertyChanges { target: root; opacity: Theme.Visible.off }
        }
    ]

    transitions: Transition {
        OpacityAnimator { duration: Theme.Animation.quick }
    }
}


