##Vertices 0-7  (x,y,z)
vertices= ( 
    (3, -.2, -1),
    (3, .2, -1),
    (-3, .2, -1),
    (-3, -.2, -1),
    (3, -.2, 1),
    (3, .2, 1),
    (-3, .2, 1),
    (-3, -.2, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,3),
    (7,4),
    (7,6)
)

surfaces = (   
    (0,1,2,3),
    (4,5,6,7),
    (1,5,4,0),
    (3,2,6,7),
    (1,2,6,5),
    (0,3,7,4)
)

colors = (
    ((1.0/255*41),(1.0/255*217),(1.0/255*152)),
    ((1.0/255*41),(1.0/255*217),(1.0/255*152)),
    ((1.0/255*242),(1.0/255*66),(1.0/255*128)),
    ((1.0/255*242),(1.0/255*66),(1.0/255*128)),
    ((1.0/255*19),(1.0/255*94),(1.0/255*242)),
    ((1.0/255*242),(1.0/255*66),(1.0/255*128)),  
)