"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""

def classFactory(iface):
    from linkit_plugin import LinkIt
    return LinkIt(iface)
