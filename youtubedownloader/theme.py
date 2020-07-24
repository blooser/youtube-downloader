from PySide2.QtCore import (
    QObject,
    Property,
    Signal,
    Slot
)

from PySide2.QtGui import (
    QColor
)


class Theme(QObject):
    colorsChanged = Signal("QVariantMap", arguments=["colors"])

    def __init__(self):
        super(Theme, self).__init__(None)

        self.properties = {
            "Colors": {
                "base": "#004d99",
                "second": "#0066cc",
                "third": "#0080ff",
                "highlight": "#3399ff",
                "text": "white",
                "placeholder": "#cccccc",
                "textStyle": "black",
                "blank": "transparent",
                "success": "#008000",
                "error": "#cc0000",
                "shadowBlack": "#99000000",
                "linkReady": "#b3b3ff"
            },

            "Margins": {
                "zero": 0,
                "tiny": 5,
                "small": 10,
                "normal": 15,
                "big": 20
            },

            "Visible": {
                "on": 1.0,
                "off": 0.0,
                "disabled": 0.4
            },

            "Size": {
                "border": 1,
                "borderBold": 2,
                "icon": 36,
                "iconSmall": 16,
                "none": 0
            },

            "Animation": {
                "hover": 50,
                "quick": 250,
                "medium": 500,
                "normal": 1000
            },

            "Time": {
                "repeat": 5000
            },

            "FontSize": {
                "groupBoxLabel": 8,
                "micro": 10,
                "tiny": 14,
                "small": 16,
                "normal": 18,
                "big": 22
            },

            "String": {
                "empty": ""
            },

            "Capacity": {
                "empty": 0
            }
        }

    @Slot(str)
    def changeBaseColor(self, color: str):
        colors_name = ["base", "second", "third", "highlight"]
        color_helper = QColor(color)

        for color_name in colors_name:
            self.properties["Colors"][color_name] = color_helper.name()
            color_helper = color_helper.lighter(130) # NOTE: 30% lighter

        self.colorsChanged.emit(self.properties["Colors"])

    @Property("QVariantMap", notify=colorsChanged)
    def Colors(self) -> dict:
        return self.properties["Colors"]

    @Property("QVariantMap", constant=True)
    def Margins(self) -> dict:
        return self.properties["Margins"]

    @Property("QVariantMap", constant=True)
    def Visible(self) -> dict:
        return self.properties["Visible"]

    @Property("QVariantMap", constant=True)
    def Size(self) -> dict:
        return self.properties["Size"]

    @Property("QVariantMap", constant=True)
    def Animation(self) -> dict:
        return self.properties["Animation"]

    @Property("QVariantMap", constant=True)
    def Time(self) -> dict:
        return self.properties["Time"]

    @Property("QVariantMap", constant=True)
    def FontSize(self) -> dict:
        return self.properties["FontSize"]

    @Property("QVariantMap", constant=True)
    def String(self) -> dict:
        return self.properties["String"]

    @Property("QVariantMap", constant=True)
    def Capacity(self) -> dict:
        return self.properties["Capacity"]
