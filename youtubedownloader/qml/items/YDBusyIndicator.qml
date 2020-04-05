import QtQuick 2.14
import QtQuick.Controls 2.14

BusyIndicator {
    id: root

    contentItem: Item {
        implicitWidth: 64
        implicitHeight: 64

        Item {
            id: item

            x: parent.width/2 - 32
            y: parent.height/2 - 32

            width: 64
            height: 64

            opacity: root.running ? Theme.Visible.on : Theme.Visible.off

            Behavior on opacity {
                OpacityAnimator {
                    duration: Theme.Animation.quick
                }
            }

            RotationAnimator {
                target: item
                running: root.visible && root.running
                from: 0
                to: 360
                loops: Animation.Infinite
                duration: 1250
            }

            Repeater {
                id: repeater
                model: 6

                Rectangle {
                    x: item.width/2 - width/2
                    y: item.height/2 - height/2

                    implicitWidth: 10
                    implicitHeight: 10

                    radius: 5
                    color: Theme.Colors.third

                    transform: [
                        Translate {
                            y: -Math.min(item.width, item.height) * 0.5 + Theme.Margins.tiny
                        },

                        Rotation {
                            angle: index/repeater.count * 360

                            origin {
                                x: Theme.Margins.tiny
                                y: Theme.Margins.tiny
                            }
                        }
                    ]
                }
            }
        }
    }
}
