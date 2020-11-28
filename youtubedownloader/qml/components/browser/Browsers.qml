﻿import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../../items" as Items

Item {
    id: root

    property var options

    readonly property var icons: {
        "Firefox": Resources.icons.firefox
        // TODO: Add more browsers icons... but after implementing reading tabs
    }

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
                    model: modelData.tabs
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
                    icon.source: icons[modelData.name]

                    Items.YDToolTip {
                        delay: 500
                        timeout: 2000
                        visible: hovered
                        text: qsTr("Current opened YouTube tabs in %1").arg(modelData.name)
                    }
                }
            }
        }
    }
}
