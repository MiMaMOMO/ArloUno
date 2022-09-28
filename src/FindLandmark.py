import robot
from time import sleep
import cv2

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

retval, frameReference = cam.read() # Read frame
    
if not retval: # Error
    print(" < < <  Game over!  > > > ")
    exit(-1)

# Show frames


arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
arucoParams = cv2.aruco.DetectorParameters_create()
corners, ids, rejected = cv2.aruco.detectMarkers(frameReference, arucoDict, parameters=arucoParams)

cv2.imshow(WIN_RF, frameReference)

print(f"corners: {corners}")
print(f"ids: {ids}")
#print(f"rejected: {rejected}")

# # Create a robot object and initialize
# arlo = robot.Robot()
# print("Running ...")
# # Arlo speed. We use the same speed here 
# leftSpeed = 64
# rightSpeed = 64
# # Send a go_diff command to drive forward.
# print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
# # The time Arlo have to rotate 90 deegrees before the next command 
# sleep(0.728)
# # Stop Arlo 
# print(arlo.stop())
# # Wait a bit before next command
# sleep(0.041)