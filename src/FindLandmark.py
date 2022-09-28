import robot
from time import sleep
import cv2
import numpy as np

def gstreamer_pipeline(capture_width=1024, capture_height=720, framerate=30):
    """Utility function for setting parameters for the gstreamer camera pipeline"""
    return (
        "libcamerasrc !"
        "video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "videoconvert ! "
        "appsink"
        % (
            capture_width,
            capture_height,
            framerate,
        )
    )


print("OpenCV version = " + cv2.__version__)

# Open a camera device for capturing
cam = cv2.VideoCapture(gstreamer_pipeline(), apiPreference=cv2.CAP_GSTREAMER)



if not cam.isOpened(): # Error
    print("Could not open camera")
    exit(-1)

# Open a window
WIN_RF = "Example 1"
cv2.namedWindow(WIN_RF)
cv2.moveWindow(WIN_RF, 100, 100)

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
arucoParams = cv2.aruco.DetectorParameters_create()
cam_matrix = np.asarray([[1600, 0, (1024/2)],[0, 1600, (720/2)],[0,0,1]])
distCoeffs = np.asarray([0,0,0,0])

while cv2.waitKey(4) == -1:
    retval, frameReference = cam.read() # Read frame
        
    if not retval: # Error
        print(" < < <  Game over!  > > > ")
        exit(-1)

    corners, ids, rejected = cv2.aruco.detectMarkers(frameReference, arucoDict, parameters=arucoParams)
    [rvecs, tvecs, obj] = cv2.aruco.estimatePoseSingleMarkers(corners, 0.1, cam_matrix, distCoeffs)
    #print(f"rvecs: {rvecs}")
    print(f"tvecs: {tvecs}")
    if tvecs is not None:
        beta = np.arccos(np.linalg.norm(tvecs) * np.asarray([0.0,0.0,1.0]))
        print(beta)



    ###VISUALISATION
    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        print(f"total ids: {ids}")
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the ArUCo detection
            cv2.line(frameReference, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frameReference, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frameReference, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frameReference, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frameReference, (cX, cY), 4, (0, 0, 255), -1)
            # draw the ArUco marker ID on the frameReference
            cv2.putText(frameReference, str(markerID),
                (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
            print("[INFO] ArUco marker ID: {}".format(markerID))
            # show the output frameReference
            
        
    cv2.imshow("frameReference", frameReference)
    

