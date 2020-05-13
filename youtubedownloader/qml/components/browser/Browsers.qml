import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property var options

    signal addTab(string url)

    implicitWidth: mainLayout.implicitWidth
    implicitHeight: mainLayout.implicitHeight

    RowLayout {
        id: mainLayout

        anchors.fill: parent
        spacing: Theme.Margins.tiny

        StackLayout {
            Layout.fillWidth: true

            currentIndex: tabBar.currentIndex

            Repeater {
                model: WebBrowsers.browsers

                BrowserTabs {
                    browser: modelData
                    options: root.options
                    onAddTab: root.addTab(url)
                }
            }
        }

        Items.YDTabBar {
            id: tabBar

            Repeater {
                model: WebBrowsers.browsers

                Items.YDTabButton {
                    text: modelData.name

                    ToolTip.delay: 500
                    ToolTip.timeout: 2000
                    ToolTip.visible: hovered
                    ToolTip.text: qsTr("Current opened YouTube tabs in %1").arg(modelData.name)
                }
            }
        }
    }
}
