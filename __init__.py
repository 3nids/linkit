"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""

def classFactory(iface):
    from linkit import LinkIt
    return LinkIt(iface)
