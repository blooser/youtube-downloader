import QtQuick 2.14

import youtubedownloader.component.changer

Loader {
    id: root

    sourceComponent: componentChanger.currentComponent

    property alias changes: componentChanger.changes

    ComponentChanger {
        id: componentChanger
    }
}
