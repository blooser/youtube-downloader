import QtQuick 2.14

Loader {
    id: root

    property bool when: false
    property Component main
    property Component second

    state: "main"
    states: [
        State {
            name: "main"
            when: !root.when
            PropertyChanges { target: root; sourceComponent: main }
        },

        State {
            name: "second"
            when: root.when
            PropertyChanges { target: root; sourceComponent: second }
        }
    ]
}
