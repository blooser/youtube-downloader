import QtQuick 2.14

import yd.items 0.1

import "../../items" as Items
import ".." as Components

Item {
    id: root

    property string searchString

    implicitWidth: listView.implicitWidth
    implicitHeight: listView.implicitHeight

    ListView {
        id: listView

        anchors.fill: parent
        boundsBehavior: Flickable.StopAtBounds
        clip: true
        spacing: Theme.Margins.tiny

        model: StringFilterModel {
            sourceModel: historyModel
            string: root.searchString
            filterRoleNames: ["title", "uploader"]
        }

        delegate: HistoryItem {
            width: listView.width

            // NOTE: To be compatible with LinkInfo.
            downloadInfo: {
                "url": url,
                "title": title,
                "uploader": uploader,
                "uploader_url": uploader_url,
                "thumbnail": thumbnail,
                "date": date
            }
        }

        remove: Transition {
            OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick  }
        }

        removeDisplaced: Transition {
            NumberAnimation { property: "y"; duration: Theme.Animation.quick }
        }

        section.property: "date"
        section.criteria: ViewSection.FullString
        section.delegate: Components.TileText {
            anchors {
                horizontalCenter: parent.horizontalCenter
            }

            font.pixelSize: 10

            text: section
        }

    }

    Items.YDText {
        anchors.centerIn: root
        text: qsTr("Empty")
        opacity: Theme.Visible.disabled
        visible: (listView.count === Theme.Capacity.empty)
    }
}
