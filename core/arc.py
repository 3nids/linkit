
from math import sin, cos, sqrt, pi
from qgis.core import QgsPoint, QgsGeometry


# offset should be  > 0


def arc(p1, p2, offset=1):

    # point in middle
    mp = QgsPoint((p1.x()+p2.x())/2, (p1.y()+p2.y())/2)
    # distance between the two points
    d = sqrt(p1.sqrDist(p2))
    # orthogonal direction to segment p1-p2
    az = (p1.azimuth(p2)+90)*pi/180
    # create point distant to segment of offset of segment length, will be center of circular arc
    cp = QgsPoint(mp.x()+d*offset*sin(az),
                  mp.y()+d*offset*cos(az))
    # radius
    r = d*sqrt(4*offset*offset+1)/2
    # calculate start and end azimuth of circular arc
    az1 = cp.azimuth(p1)
    az2 = cp.azimuth(p2)
    if az2 < az1:
        az2 += 360
    # draw arc
    vx = [cp.x()+r*sin(az*pi/180) for az in floatrange(az1, az2, 5)]
    vy = [cp.y()+r*cos(az*pi/180) for az in floatrange(az1, az2, 5)]
    arcLine = [QgsPoint(vx[i], vy[i]) for i in range(len(vx))]
    return QgsGeometry().fromPolyline(arcLine)


def floatrange(a, b, step):
    while a < b:
        yield a
        a += step
    yield b