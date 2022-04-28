from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
    Property
 )
from PySide6.QtQml import (
    QQmlParserStatus,
    QmlElement,
    QQmlComponent,
    QQmlListReference,
    ListProperty
)
from PySide6 import QtWidgets
from PySide6 import QtQuick


from youtubedownloader.logger import create_logger

logger = create_logger("youtubedownloader.component_changer")

QML_IMPORT_NAME = "youtubedownloader.component.changer"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Change(QObject):
    activated = Signal(QQmlComponent)
    whenChanged = Signal(bool)
    componentChanged = Signal(QQmlComponent)

    def __init__(self):
        super().__init__(None)

        self._when = False
        self._component = QQmlComponent()

    @Property("bool", notify = whenChanged)
    def when(self):
        return self._when

    @when.setter
    def when(self, w):
        self._when = w
        self.whenChanged.emit(self._when)

        if self._when:
            self.activated.emit(self._component)

    @Property("QVariant", notify = componentChanged)
    def component(self):
        return self._component

    @component.setter
    def component(self, c):
        self._component = c
        self.componentChanged.emit(self._component)



@QmlElement
class ComponentChanger(QObject):
    currentComponentChanged = Signal(QQmlComponent)

    def __init__(self):
        super(ComponentChanger, self).__init__(None)

        self._current_component = None
        self._changes = []

    @Property(Change, notify=currentComponentChanged)
    def currentComponent(self):
        return self._current_component

    @Slot(QQmlComponent)
    def setCurrentComponent(self, component):
        if not component:
            logger.warning("Component is none!")

            return

        self._current_component = component
        self.currentComponentChanged.emit(self._current_component)

        logger.info(f"Current component changed for {self._current_component}")

    def appendChange(self, change):
        change.activated.connect(self.setCurrentComponent)
        self._changes.append(change)

    changes = ListProperty(Change, appendChange)
