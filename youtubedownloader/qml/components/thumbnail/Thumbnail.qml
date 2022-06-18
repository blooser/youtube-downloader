import QtQuick 2.14
import QtQuick.Layouts 1.15

import yd.items 0.1

import youtubedownloader.download


import "../../items" as Items
import "../dynamic" as Dynamic
import "../buttons" as Buttons

Item {
    id: root

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    property url source

    signal close()

    ColumnLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.big

        Items.YDImage {
            fillMode: Image.Stretch
            source: root.source

            MouseArea {
                anchors.fill: parent
                onClicked: root.close()
            }
        }

        ThumbnailDownloadButton {
            Layout.alignment: Qt.AlignHCenter

            visible: !downloader.downloading

            onDownload: (path) => {
                downloader.download(root.source, path)
            }
        }

        ThumbnailDownloadingProgress {
            id: downloadingProgress

            Layout.fillWidth: true
            Layout.preferredHeight: 24

            visible: downloader.downloading

            to: 100
            value: downloader.progress
            from: 0

            destination: downloader.destination
        }

        ThumbnailOpen {
            id: thumbnailOpen

            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: Theme.Size.icon
            Layout.preferredHeight: Theme.Size.icon

            onOpen: Qt.openUrlExternally(downloader.destination)

            state: downloader.progress >= 100 ? "in" : "out"

        }
    }

    ThumbnailDownloader {
        id: downloader
    }
}



