import cv2

### ARUCO ### 
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
ARUCO_MARKER_LENGTH = 0.15

### PATHS ### 


### TITLES ###
WIN_RF1 = "Robot view"              # The title for Arlos window 
WIN_World = "World view"            # The title for the worlds window

### WINDOWS ###
ARLO_WIN_X = 50                     # X-coordinate for Arlos window 
ARLO_WIN_Y = 50                     # Y-coordinate for Arlos window
WORLD_WIN_X = 500                   # X-coordinate for the world window
WORLD_WIN_Y = 50                    # Y-coordinate for the world window

### ARLO ###


### LANDMARKS ###
landmarkIDs = [1, 2, 3, 4]          # The ID of each landmark we know  
LANDMARKS = {
    1: (0.0, 0.0),                  # Coordinates for landmark 1 (RED)
    2: (0.0, 300.0),                # Coordinates for landmark 2 (GREEN)
    3: (400.0, 0.0),                # Coordinates for landmark 3 (BLUE)
    4: (400.0, 300.0)               # Coordinates for landmark 4 (BLACK)
}

### PARTICLES ###
NUM_OF_PARTICLES = 1000             # The number of particles in the world 

### UNCERTAINITY ###
SIGMA_UNCERTAINITY = 1.0            # Uncertainity added to sigma for distance 
THETA_UNCERTAINITY = 0.01           # Uncertainity added to theta for orientation 

### VELOCITY ###
VELOCITY = 0                        # ???
ANGULAR_VELOCITY = 0                # ???
RIGHT_VELOCITY = 64                 # Arlos right wheel speed
LEFT_VELOCITY = 64                  # Arlos left wheel speed
RIGHT_ROT_VELOCITY = 64             # Arlos right wheel rotation speed
LEFT_ROT_VELOCITY = 64              # Arlos left wheel rotation speed

### DISTANCE ###
METER = 2.52                        # How long it takes Arlo to drive one meter in seconds

### ORIENTATION ###
ORIENTATION = 2.912                 # How long it takes Arlo to rotate 360 degrees

### SPREADS ###
SPREAD_DIST = 15.0                  # The spread used when computing distance weights 
SPREAD_ANGLE = 1.0                  # The spread used when computing orientation weights 

### COLORS ### 
CRED = (0, 0, 255)                  # The color red 
CGREEN = (0, 255, 0)                # The color green 
CBLUE = (255, 0, 0)                 # The color blue 
CCYAN = (255, 255, 0)               # The color cyan 
CYELLOW = (0, 255, 255)             # The color yellow
CMAGENTA = (255, 0, 255)            # The color magenta
CWHITE = (255, 255, 255)            # The color white 
CBLACK = (0, 0, 0)                  # The color black 

### TIMER ### 
