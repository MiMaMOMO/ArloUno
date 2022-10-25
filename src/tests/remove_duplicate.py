# TODO: Mikkel fixes this 

def remove_duplicate(objectIDs, dists, angles, landmarks):
    '''
    ... 
    '''
    if objectIDs is not None:
        known_dists = [dist for dist, id in zip(dists, objectIDs) if id in landmarks]
        known_angles = [angle for angle, id in zip(angles, objectIDs) if id in landmarks]            
        #known_objectIDs = [id for id in objectIDs if id in landmarks] if len(objectIDs) == 0 : objectIDs = None
        
    return known_dists, known_angles
