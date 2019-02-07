#Config File for storing Robot "Global" Variables

#Wheels
MAX_SPEED_W = 400 #Max speed that the wheels can spin out of 1000
MAX_DELTA_W = 100 #Max safe stoping deceleration of the wheels
MAX_DPAD_W  = 200 #Max speed the Dpad can drive at

#Drum
MAX_SPEED_D = 1000 #Max speed that the drumm can spin out of 1000
MAX_STOP_D = 150  #Max safe stoping deceleration of the drum
MAX_DELTA_D = 100 #Speed incrimintation for the drum

#Old Joystick variables
old_joystick_1 = 0 #(Circle)   - Drum forwards
old_joystick_2 = 0 #(Square)   - Drum backwards
old_joystick_3 = 0 #(Triangle) - FULL_ESTOP toggle
old_joystick_6 = 0 #(Select)   - DEBUG_ESTOP toggle
old_joystick_7 = 0 #(start)    - DRIVE_ESTOP toggle
old_hat_0 = (0,0)  #(Dpad)     - Driving controls

#Old Keyboard variables
old_K_1 = 0
old_K_ESCAPE = 0
old_K_BACKQUOTE = 0
old_K_KP3 = 0
old_K_KP6 = 0

#Estop
FULL_ESTOP = 1  #You can figure out what
DRIVE_ESTOP = 1 #these three variables are
DEBUG_ESTOP = 0 #I believe in you!

#Colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)

#Size
SIZE1 = [300,250] #Screen size w/o joystick display
SIZE2 = [300,625] #Screen size w/ joystick display
