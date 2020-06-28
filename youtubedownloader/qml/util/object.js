function createObject(component, parent, properties) {
    return component.createObject(parent, properties)
}

function createComponent (url, parent, properties, callback=null) {
    var component = Qt.createComponent(url)

    if (component.status === Component.Error) {
        console.warn("Failed to create", url, component.errorString())
        return
    }

    if (typeof callback === "function") {
        properties["callback"] = callback
    }

    return createObject(component, parent, properties)
}
