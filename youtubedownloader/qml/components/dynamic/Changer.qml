import QtQuick 2.14

import yd.items 0.1

Loader {
    id: root

    sourceComponent: componentChanger.currentComponent

    property alias changes: componentChanger.changes

    ComponentChanger {
        id: componentChanger
    }
}
