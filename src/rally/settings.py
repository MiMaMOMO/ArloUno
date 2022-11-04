# from cv2 import aruco

# # TODO: Spread this information out after testing and project end
# # TODO: Consider using other data structures for storing data
# # TODO: Remember that Arlo can only see up to approximatly 62 cm, below that and Arlo cannot see the landmarks which means Arlo cannot detect them.     

# ### SETTINGS ###
# SHOW_GUI = False          # Whether or not to open GUI windows
# ON_ROBOT = True          # Whether or not we are running on the Arlo robot


# ### ARUCO ### 
# ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
# ARUCO_MARKER_LENGTH = 0.15


# ### TITLES ###
# WIN_RF1 = "Robot view"              # The title for Arlos window 
# WIN_WORLD = "World view"            # The title for the worlds window


# ### WINDOWS ###
# ARLO_WIN_X = 50                     # X-coordinate for Arlos window 
# ARLO_WIN_Y = 50                     # Y-coordinate for Arlos window
# WORLD_WIN_X = 500                   # X-coordinate for the world window
# WORLD_WIN_Y = 50                    # Y-coordinate for the world window


# ### LANDMARKS ### 
# RUTE = [1, 2, 3, 4, 1]              # The rute we wanna take 
# LANDMARK_IDS = [1, 2, 3, 4]         # The ID of each landmark we know  
# LANDMARKS = {
#     1: (0.0, 0.0),                  # Coordinates for landmark 1 (RED)
#     2: (0.0, 300.0),                # Coordinates for landmark 2 (GREEN)
#     3: (400.0, 0.0),                # Coordinates for landmark 3 (BLUE)
#     4: (400.0, 300.0)               # Coordinates for landmark 4 (BLACK)
# }
# OBSTACLES = {
#     5: {0.0, 0.0},
#     6: {0.0, 0.0},
#     7: {0.0, 0.0},
#     8: {0.0, 0.0},
#     9: {0.0, 0.0},
#     10: {0.0, 0.0},
#     11: {0.0, 0.0}
# }


# ### PARTICLES ###
# NUM_OF_PARTICLES = 3000             # The number of particles in the world 


# ### UNCERTAINITY ###
# SIGMA_UNCERTAINITY = 2.0            # Uncertainity added to sigma for distance 
# THETA_UNCERTAINITY = 0.1            # Uncertainity added to theta for orientation 


# ### VELOCITY ###
# RIGHT_VELOCITY = 67                 # Arlos right wheel speed
# LEFT_VELOCITY = 61                  # Arlos left wheel speed
# RIGHT_ROT_VELOCITY = 64             # Arlos right wheel rotation speed
# LEFT_ROT_VELOCITY = 64              # Arlos left wheel rotation speed


# ### ROTATIONS ### 
# DEGREES_13 = 0.156892               # 13 degrees in radions
# DEGREES_15 = 0.261799               # 15 degrees in radions
# DEGREES_20 = 0.349065               # 20 degrees in radions
# DEGREES_30 = 0.523598               # 30 degrees in radions 
# DEGREES_45 = 0.785398               # 45 degrees in radions
# DEGREES_90 = 1.57175                # 90 degrees in radions 
# DEGREES_120 = 2.09439               # 120 degrees in radions 
# DEGREES_180 = 3.14255               # 180 degrees in radions
# DEGREES_240 = 4.18879               # 240 degrees in radions
# DEGREES_270 = 4.72234               # 270 degrees in radions
# DEGREES_310 = 5.41052               # 310 degrees in radions
# DEGREES_360 = 6.28414               # 360 degrees in radions
# FULL_ROTATION = 50                  # How many times it take Arlo to do a 360 degree rotation


# ### DISTANCES ### 
# HALF_METER = 50.0                   # 0.5 meter in cm 
# ONE_METER = 100.0                   # 1 meter in cm 
# TWO_METER = 200.0                   # 2 meter in cm 
# THREE_METER = 300.0                 # 3 meter in cm
# LANDMARK_RANGE = 0.4                # Arlo should always try to come within 40 cm of a landmark


# ### SPREADS ###
# SPREAD_DIST = 15.0                  # The spread used when computing distance weights 
# SPREAD_ANGLE = 2.0                  # The spread used when computing orientation weights 

# ### COLORS ### 
# CRED = (0, 0, 255)                  # The color red 
# CGREEN = (0, 255, 0)                # The color green 
# CBLUE = (255, 0, 0)                 # The color blue 
# CCYAN = (255, 255, 0)               # The color cyan 
# CYELLOW = (0, 255, 255)             # The color yellow
# CMAGENTA = (255, 0, 255)            # The color magenta
# CWHITE = (255, 255, 255)            # The color white 
# CBLACK = (0, 0, 0)                  # The color black 
# LANDMARK_COLORS = [                 # Colors of the known landmarks 
#     CRED, 
#     CGREEN,
#     CBLUE,
#     CCYAN
# ]

# ### TIME ### 
# TIME_ERROR = 0.55                   # Error in computing time 
# TIME_METER = 2.52                   # How long it takes Arlo to drive one meter in seconds
# TIME_ORIENTATION = 0.728            # How long it takes Arlo to rotate 90 degrees

from cv2 import aruco

# TODO: Spread this information out after testing and project end
# TODO: Consider using other data structures for storing data

### SETTINGS ###
SHOW_GUI = True          # Whether or not to open GUI windows
ON_ROBOT = True          # Whether or not we are running on the Arlo robot


### ARUCO ### 
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
ARUCO_MARKER_LENGTH = 0.15


### TITLES ###
WIN_RF1 = "Robot view"              # The title for Arlos window 
WIN_WORLD = "World view"            # The title for the worlds window


### WINDOWS ###
ARLO_WIN_X = 50                     # X-coordinate for Arlos window 
ARLO_WIN_Y = 50                     # Y-coordinate for Arlos window
WORLD_WIN_X = 500                   # X-coordinate for the world window
WORLD_WIN_Y = 50                    # Y-coordinate for the world window


### LANDMARKS ### 
RUTE = [1, 2, 3, 4, 1]              # The rute we wanna take 
LANDMARK_IDS = [1, 2, 3, 4]         # The ID of each landmark we know  
LANDMARKS = {
    1: (0.0, 0.0),                  # Coordinates for landmark 1 (RED)
    2: (0.0, 300.0),                # Coordinates for landmark 2 (GREEN)
    3: (400.0, 0.0),                # Coordinates for landmark 3 (BLUE)
    4: (400.0, 300.0)               # Coordinates for landmark 4 (BLACK)
}


### PARTICLES ###
NUM_OF_PARTICLES = 3000             # The number of particles in the world 


### UNCERTAINITY ###
SIGMA_UNCERTAINITY = 2.0            # Uncertainity added to sigma for distance 
THETA_UNCERTAINITY = 0.1            # Uncertainity added to theta for orientation 


### VELOCITY ###
RIGHT_VELOCITY = 67                 # Arlos right wheel speed
LEFT_VELOCITY = 61                  # Arlos left wheel speed
RIGHT_ROT_VELOCITY = 64             # Arlos right wheel rotation speed
LEFT_ROT_VELOCITY = 64              # Arlos left wheel rotation speed


### ROTATIONS ### 
DEGREES_15 = 0.261799               # 15 degrees in radions
DEGREES_20 = 0.349065               # 20 degrees in radions
DEGREES_30 = 0.523598               # 30 degrees in radions 
DEGREES_45 = 0.785398               # 45 degrees in radions
DEGREES_90 = 1.57175                # 90 degrees in radions 
DEGREES_120 = 2.09439               # 120 degrees in radions 
DEGREES_180 = 3.14255               # 180 degrees in radions
DEGREES_240 = 4.18879               # 240 degrees in radions
DEGREES_270 = 4.72234               # 270 degrees in radions
DEGREES_310 = 5.41052               # 310 degrees in radions
DEGREES_360 = 6.28414               # 360 degrees in radions
FULL_ROTATION = 50                  # How many times it take Arlo to do a 360 degree rotation


### DISTANCES ### 
HALF_METER = 50.0                   # 0.5 meter in cm 
ONE_METER = 100.0                   # 1 meter in cm 
TWO_METER = 200.0                   # 2 meter in cm 
THREE_METER = 300.0                 # 3 meter in cm
LANDMARK_RANGE = 0.4                # Arlo should always try to come within 40 cm of a landmark


### SPREADS ###
SPREAD_DIST = 15.0                  # The spread used when computing distance weights 
SPREAD_ANGLE = 2.0                  # The spread used when computing orientation weights 

### COLORS ### 
CRED = (0, 0, 255)                  # The color red 
CGREEN = (0, 255, 0)                # The color green 
CBLUE = (255, 0, 0)                 # The color blue 
CCYAN = (255, 255, 0)               # The color cyan 
CYELLOW = (0, 255, 255)             # The color yellow
CMAGENTA = (255, 0, 255)            # The color magenta
CWHITE = (255, 255, 255)            # The color white 
CBLACK = (0, 0, 0)                  # The color black 
LANDMARK_COLORS = [                 # Colors of the known landmarks 
    CRED, 
    CGREEN,
    CBLUE,
    CCYAN
]

### TIME ### 
TIME_ERROR = 0.55                   # Error in computing time 
TIME_METER = 2.52                   # How long it takes Arlo to drive one meter in seconds
TIME_ORIENTATION = 0.728            # How long it takes Arlo to rotate 90 degrees
