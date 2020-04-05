import QtQuick 2.14

Loader {
    id: root

    property bool when: false
    property Component main
    property Component second

    states: [
        State {
            when: !root.when
            PropertyChanges { target: root; sourceComponent: main }
        },

        State {
            when: root.when
            PropertyChanges { target: root; sourceComponent: second }
        }
    ]
}
