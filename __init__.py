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
    return "Associates feature ID to another feature field. This plugin requires ItemBrowser plugin."
def version():
    return "Version 1.0"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.7"
def classFactory(iface):
    # load Sige class from file Sige
    from linkit import LinkIt
    return LinkIt(iface)
