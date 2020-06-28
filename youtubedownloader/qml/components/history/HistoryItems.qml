import QtQuick 2.14

Item {
    id: root

    implicitWidth: listView.implicitWidth
    implicitHeight: listView.implicitHeight

    ListView {
        id: listView

        anchors.fill: parent
        boundsBehavior: Flickable.StopAtBounds
        clip: true
        spacing: Theme.Margins.tiny

        model: historyModel

        delegate: HistoryItem {
            width: listView.width

            link: url
            titleText: title
            uploaderText: uploader
            uploaderLink: uploaderUrl
            thumbnailSource: thumbnail
        }
    }
}
