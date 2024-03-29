import QtQuick 2.14
import QtQuick.Layouts 1.12

import "../../items" as Items
import "../link" as Link
import "../format" as Format
import "../buttons" as Buttons
import ".." as Components

Rectangle {
    id: root

    property var pendingInfo
    property var pendingOptions

    signal formatSelected(string format)
    signal changeOutput(string path)
    signal remove()

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    color: downloadManager.pendingModel.duplicate.url === root.pendingInfo.url ? "orange" : Theme.Colors.second

    border {
        width: Theme.Size.border
        color: Theme.Colors.base
    }

    RowLayout {
        id: mainLayout

        anchors {
            fill: parent
            leftMargin: Theme.Margins.normal
            rightMargin: Theme.Margins.normal
        }

        spacing: Theme.Margins.big

        Link.LinkInfo {
            id: link

            info: root.pendingInfo

            Layout.fillWidth: true
        }

        Format.FormatSelected {
            Layout.preferredWidth: Theme.Size.format

            options: root.pendingOptions

            onFormatSelected: format => {
                root.formatSelected(format)
            }
        }

        Buttons.DeleteButton {
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            onRemove: root.remove()
        }
    }

    PendingOutput {
        anchors {
            horizontalCenter: root.horizontalCenter
            bottom: root.bottom
        }

        itemOptions: root.pendingOptions
        itemInfo: root.pendingInfo

        onChangeOutput: path => { root.changeOutput(path) }
    }

    Behavior on color {
        ColorAnimation {
            duration: Theme.Animation.quick
        }
    }
}
