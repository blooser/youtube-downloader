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
        filterRoleName: "name"
    }

    delegate: Items.YDText {
        width: root.width
        text: name
    }

    ScrollBar.vertical: Items.YDScrollBar {}
}
