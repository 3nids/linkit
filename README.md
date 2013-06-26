## What ? 

Link It is a [QGIS](http://www.qgis.org) plugin to link a feature to another. 

The idea is to copy in a chosen field the ID of a feature by clicking on it.

## How ?

A demo is visible on [youtube](http://www.youtube.com/watch?v=wNfiNvlhNvo&hd=1).

1. First, create a link in the _links manager_. Be aware, that only one link per layer can be created.
2. A corresponding feature action is available for the destination layer
3. Select this action, then choose a feature
4. A dock appears on the left
5. Click on the arrow icon and select the desired feature on map
6. You can delete this link using the corresponding icon
7. The plugin can also draw the link by activating the arrow icon


## Tip

If you want to have a postgis layer drawing a nice arrow from one feature (child) to another (parent), here you go.
Just change the values between underscores. 

	CREATE OR REPLACE VIEW _schema_._view_name_ AS
		SELECT child, parent,
			 ST_CurveToLine(ST_GeomFromEWKT('SRID=_YOURSRID_;CIRCULARSTRING('
				||ST_X(start_point)||' '||ST_Y(start_point)
				||','||
				ST_X(middle_point)+distance*cos(azimuth)||' '||ST_Y(middle_point)+distance*sin(azimuth)
				||','||
				ST_X(end_point)||' '||ST_Y(end_point) 
				||')'
			),15)::geometry(LineString,21781) AS wkb_geometry
		FROM (
			SELECT child,parent,
				start_point , end_point ,
				pi()/2+ST_Azimuth(start_point,end_point) AS azimuth,
				.5*ST_Distance(start_point,end_point) AS distance,
				ST_Line_Interpolate_Point(ST_MakeLine( start_point , end_point ),.5)::geometry(Point,21781) AS middle_point
			FROM (
				SELECT a.id AS child ,b.id AS parent, 
						ST_Line_Interpolate_Point(a.wkb_geometry,.5)::geometry(Point,21781) AS start_point,
						/* select end_point at 4 meters from the closest side of the pipe */
						ST_ClosestPoint(ST_MakeLine(  
							ST_Line_Interpolate_Point(b.wkb_geometry,   LEAST(1,  4/b._length2d/2))::geometry(Point,21781) ,
							ST_Line_Interpolate_Point(b.wkb_geometry,GREATEST(0,1-4/b._length2d/2))::geometry(Point,21781) 
						),a.wkb_geometry) AS end_point
				FROM _yourschema_._yourtable_ a 
				INNER JOIN _yourschema_._yourtable_ b ON a._fieldOfParentID_ = b.id
				WHERE a.id_parent IS NOT NULL
			) AS foo
		) AS foo2;

