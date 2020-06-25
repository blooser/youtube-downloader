import QtQuick 2.14

YDButton {
    property alias imageSource: image.source

    contentItem: YDImage {
        id: image
    }
}
