import QtQuick 2.14

import "../../items" as Items

Items.YDButton {
    id: root

    signal download(url path)

    text: "Download"

    onClicked: {
        dialogManager.openDialog("SelectFileDialog", {}, function(file){
            let path = Paths.cleanPath(file)

            root.download(path)
         })
    }

    Component.onCompleted: root.state = "in"

    opacity: 0
    scale: 0.5

    states: [
        State {
            name: "in"

            PropertyChanges {
                target: root

                opacity: 1
                scale: 1

            }
        }
    ]

    transitions: [
        Transition {
            SequentialAnimation {
                PauseAnimation { duration: Theme.Animation.quick }
                ParallelAnimation {
                    OpacityAnimator { duration: Theme.Animation.quick  }
                    ScaleAnimator {  duration: Theme.Animation.quick }
                }
            }
        }
    ]
}
