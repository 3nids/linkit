"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""
def name():
    return "Link It"
def description():
    return "To link a feature to another. By clicking on map, the plugin will then automatically save the feature's ID in the appropriate field defined by the user. [This plugin requires ItemBrowser]"
def version():
    return "Version 1.1.1"
def icon():
    return "icons/linkit.png"
def qgisMinimumVersion():
    return "1.7"
def classFactory(iface):
    from linkit import LinkIt
    return LinkIt(iface)
