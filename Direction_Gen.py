import numpy as np
def next_direction(desired_direction, radar):
    # blocking map, first column is indicator, if there's object within 0.5meter, indicator set to be 0
    # second column angle
    # third column angle distance, if there's no object within 0.5meter
    blocking=np.ones((len(radar),3))
    for i, item in enumerate(radar):
        blocking[i][1]=item[0]
        blocking[i][2]=360
        if item[1]>50:
            blocking[i][0]=0
        else:
            tmp=abs(desired_direction-item[0])
            if tmp>180:
                blocking[i][2]=tmp%180
            else:
                blocking[i][2]=tmp
    # find closest direction
    m = 360
    angle = 0
    for i,item in enumerate(blocking):
        if item[0]==1:
            if item[2]<m:
                m=item[2]
                angle=item[1]
    return(angle)
