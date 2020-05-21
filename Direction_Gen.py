import numpy as np
def next_direction(desired_direction, radar):
    # blocking map, first column is indicator, if there's object within 0.5meter, indicator set to be 0
    # second column angle
    # third column angle distance, if there's no object within 0.5meter
    blocking=np.ones((len(radar),3))
    for i, item in enumerate(radar):
        blocking[i][1]=item[0]
        blocking[i][2]=180
        if item[1]<100:
            blocking[i][0]=0
        else:
            tmp=item[0]#abs(desired_direction-item[0])
            if tmp>180:
                blocking[i][2]=tmp-360
            else:
                blocking[i][2]=tmp
    # find closest direction
    m = 180
    angle = 0
    for i,item in enumerate(blocking):
        if item[0]==1:
            if abs(item[2])<abs(m):
                m=item[2]
                angle=item[2]
    return(angle)