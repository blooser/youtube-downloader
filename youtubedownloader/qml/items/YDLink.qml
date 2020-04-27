import QtQuick 2.14

YDText {
    id: root

    property string link

    readonly property var isUrl: function (url) {
        let matches = url.match(/^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/)
        return (matches !== null && matches.length > Theme.Size.none)
    }

    MouseArea {
        id: linkMouseArea

        anchors.fill: parent

        hoverEnabled: true
        enabled: isUrl(link)
        onClicked: Qt.openUrlExternally(link)
    }

    states: State {
        when: linkMouseArea.containsMouse
        PropertyChanges { target: root; color: Theme.Colors.linkReady }
    }

    transitions: Transition {
        ColorAnimation { duration: Theme.Animation.quick }
    }
}
