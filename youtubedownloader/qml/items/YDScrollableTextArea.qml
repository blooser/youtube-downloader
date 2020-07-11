import QtQuick 2.14
import QtQuick.Controls 2.14

YDScrollView {
    id: root

    property alias text: textArea.text
    property alias placeholderText: textArea.placeholderText
    property alias placeholderTextColor: textArea.placeholderTextColor

    implicitHeight: textArea.background.implicitHeight

    clip: true

    passiveColor: Theme.Colors.third
    activeColor: Theme.Colors.highlight

    function clear() {
        textArea.clear()
    }

    YDTextArea {
        id: textArea

        focus: root.focus
    }
}
