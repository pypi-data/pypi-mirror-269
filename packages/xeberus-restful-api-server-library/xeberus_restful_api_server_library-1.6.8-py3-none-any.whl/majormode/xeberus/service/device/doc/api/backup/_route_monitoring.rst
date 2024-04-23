================
Route Monitoring
================

Xeberus allows an organization to edit the *route* that a vehicle of this organization will be required to follow.

A *route* is defined by a *path* and two or more *waypoints*. A *waypoint* is either a *control point* or a *checkpoint*:

* **control points**: when a user defines a route, he generally starts with specifying a departure and an arrival points. The route editor tool automatically chooses what it thinks to be the most optimized path between these two points. However the user might want this path to be different, he might want the vehicle to follow some other roads. The user can then define a few points that the path needs to pass by. The route editor tool will then adjust the path to respect the user's requirements. Some route segments might correspond to the exact path the user wants the vehicle to follow, some others might not. The user can then specify additional *control points* to adjust the path for the segments that didn't exactly correspond to what the user wants.

* **checkpoints**: checkpoints are specific points on a path that are used to raise a notification when the vehicle, following this path, arrives to or leaves one of these points. A *checkpoint* can be a *control point*, but not necessarily. Checkpoints have an index from 0 to the number of waypoints minus ``1`` of the route. Checkpoints can be defined a name, but not necessarily. When no named is defined, the default name ``Checkpoint n``, where ``n`` is the index of this checkpoint, is used.

A *route* must be given a name. This name must be unique among all the *routes* that the organization has defined. The case is insensitive.

