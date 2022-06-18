import QtQuick 2.14
import QtQuick.Layouts 1.15

import "../buttons" as Buttons



Buttons.OpenButton {
    id: root

    states: [
        State {
            name: "in"

            PropertyChanges {
                target: root

                opacity: 1
                scale: 1
            }
        },

        State {
            name: "out"

            PropertyChanges {
                target: root

                opacity: 0
                scale: 0
            }
        }

    ]

    transitions: [
        Transition {
            ParallelAnimation {
                OpacityAnimator { duration: Theme.Animation.medium }
                ScaleAnimator  { duration: Theme.Animation.medium }
            }
        }
    ]
}
