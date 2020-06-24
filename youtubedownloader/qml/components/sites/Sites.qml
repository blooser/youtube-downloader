import QtQuick 2.14

import "../../items" as Items

ListView {
    id: root

    clip: true
    spacing: Theme.Margins.tiny
    boundsBehavior: Flickable.StopAtBounds

    model: supportedSitesDownloader.supportedSites

    delegate: Items.YDText {
        width: root.width
        text: modelData
    }
}
