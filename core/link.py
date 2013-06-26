
from qgis.core import QgsMapLayerRegistry, QgsAction


def getLink(layer):
    name = layer.customProperty("LinkIt_name", "")
    destField = layer.customProperty("LinkIt_destinationField", "")
    sourceLayer = layer.customProperty("LinkIt_sourceLayer", "")
    return Link(name, layer.id(), destField, sourceLayer)


class Link():
    def __init__(self, name, destinationLayer, destinationField, sourceLayer):
        self.name = name
        self.destinationLayer = QgsMapLayerRegistry.instance().mapLayer(destinationLayer)
        self.destinationField = destinationField
        self.sourceLayer = QgsMapLayerRegistry.instance().mapLayer(sourceLayer)

    def check(self):
        if self.destinationLayer is None:
            return False
        if self.destinationLayer.fieldNameIndex(self.destinationField) == -1:
            return False
        if self.sourceLayer is None:
            return False
        return True

    def save(self):
        self.destinationLayer.setCustomProperty("LinkIt_name", self.name)
        self.destinationLayer.setCustomProperty("LinkIt_destinationField", self.destinationField)
        self.destinationLayer.setCustomProperty("LinkIt_sourceLayer", self.sourceLayer.id())
        self.createAction()

    def createAction(self):

        actionStr = "qgis.utils.plugins['linkit'].linkit('%s','%s','%s', [%% $id %%])" % (self.destinationLayer.id(),
                                                                                          self.destinationField,
                                                                                          self.sourceLayer.id())
        self.deleteAction()
        actions = self.sourceLayer.actions()
        actions.addAction(QgsAction.GenericPython, self.name, actionStr)

    def deleteAction(self):
        actions = self.sourceLayer.actions()
        while True:
            for i in range(actions.size()):
                if "qgis.utils.plugins['linkit'].linkit(" in actions[i].action():
                    actions.removeAction(i)
                    continue
            break

    def delete(self):
        self.destinationLayer.setCustomProperty("LinkIt_name", "")
        self.destinationLayer.setCustomProperty("LinkIt_destinationField", "")
        self.destinationLayer.setCustomProperty("LinkIt_sourceLayer", "")
        self.deleteAction()



