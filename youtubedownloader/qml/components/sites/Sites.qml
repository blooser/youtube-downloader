import QtQuick 2.14
import QtQuick.Controls 2.14

import yd.items 0.1

import "../../items" as Items

ListView {
    id: root

    property string site

    clip: true
    spacing: Theme.Margins.tiny
    boundsBehavior: Flickable.StopAtBounds

    model: StringFilterModel {
        sourceModel: supportedSitesModel
        string: root.site
        filterRoleNames: ["name"]
    }

    delegate: Items.YDText {
        width: root.width
        text: name
    }

    Items.YDText {
        anchors.centerIn: root
        text: qsTr("Empty")
        visible: (root.count === Theme.Capacity.empty)
        opacity: Theme.Visible.disabled
    }

    remove: Transition {
        OpacityAnimator { from: Theme.Visible.on; to: Theme.Visible.off; duration: Theme.Animation.quick }
    }

    removeDisplaced: Transition {
        NumberAnimation { property: "y"; duration: Theme.Animation.quick }
    }

    ScrollBar.vertical: Items.YDScrollBar {}
}
