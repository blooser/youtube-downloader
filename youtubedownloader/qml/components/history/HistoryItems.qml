import QtQuick 2.14

import yd.items 0.1


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
            filterRoleName: "title"
        }

        delegate: HistoryItem {
            width: listView.width

            link: url
            titleText: title
            uploaderText: uploader
            uploaderLink: uploaderUrl
            thumbnailSource: thumbnail
        }

        remove: Transition {
            OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick  }
        }

        removeDisplaced: Transition {
            NumberAnimation { property: "y"; duration: Theme.Animation.quick }
        }
    }
}
