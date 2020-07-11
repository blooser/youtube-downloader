import QtQuick 2.14
import QtQuick.Controls 2.14

YDScrollView {
    implicitHeight: textArea.background.implicitHeight
    clip: true

    YDTextArea {
        id: textArea
    }
}
