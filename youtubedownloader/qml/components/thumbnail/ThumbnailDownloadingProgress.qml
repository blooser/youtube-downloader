import QtQuick 2.14
import QtQuick.Layouts 1.15

import "../../items" as Items
import ".." as Components
import "../../util/numbers.js" as Numbers



Items.YDProgressBar {
    id: root

    property string destination

    radius: (implicitWidth/implicitHeight)

    Items.YDText {
        anchors.centerIn: parent

        text: root.destination

        style: Text.Raised
        styleColor: "black"

        z: root.z + 1
    }

    Behavior on value {
        NumberAnimation { duration: Theme.Animation.medium }
    }
}






