import pygame
import PyCmdMessenger
import TextPrint
import CF
import Display
import JoystickInput
import KeyboardInput

#SET-UP-Arduino------------------------------------------------------------
Arduino = False

if (Arduino):
    commands = [["shoulder","i"],
                ["elbow","i"],
                ["left_F","i"],
                ["left_B","i"],
                ["right_F","i"],
                ["right_B","i"],
                ["drum","i"],
                ["FULL_ESTOP","i"],
                ["DRIVE_ESTOP","i"],
                ["DEBUG_ESTOP","i"]]

    arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=9600)
    c = PyCmdMessenger.CmdMessenger(arduino,commands)

    #msg read out (prints a msg from the Arduino)
    msg_readout = 0
    msg_interval = 1 #skips this many frames

#SET_UP-Pygame-------------------------------------------------------------

pygame.init()
pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#SET_UP-Variables----------------------------------------------------------

#initalize "actual" motor variables
shoulder_value_a = 0.0
elbow_value_a = 0.0
left_F_value_a = 0.0
left_B_value_a = 0.0
right_F_value_a = 0.0
right_B_value_a = 0.0
drum_value_a = 0.0

#initalize motor "goal" variables
shoulder_value_g = 0.0
elbow_value_g = 0.0
left_F_value_g = 0.0
left_B_value_g = 0.0
right_F_value_g = 0.0
right_B_value_g = 0.0
drum_value_g = 0.0
goals = [shoulder_value_g,
         elbow_value_g,
         left_F_value_g,
         left_B_value_g,
         right_F_value_g,
         right_B_value_g,
         drum_value_g]

#SET_UP-Joysticks----------------------------------------------------------

# Get count of joysticks
joystick_count = pygame.joystick.get_count()

if (joystick_count == 0): #if no joystick conected
    print("NO JOYSTICK CONNECTED!")
    print("You can still drive with keyboard controls")
    print("Esc     = ESTOP")
    print("~       = Drive_ESTOP")
    print("1       = DEBUG_ESTOP")
    print("wasd    = wheels")
    print("KP1&4   = Shoulder")
    print("KP2&5   = Elbow")
    print("KP0&3&6 = Drum")
elif(joystick_count == 1): #if one joystick conected
    print("ONE joystick conected")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else: #if to many joysticks conected
    print("TO MANY JOYSTICK CONNECTED!")
    done = True

#Main Program Loop---------------------------------------------------------

while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    #resets the goal variables
    goals[0] = 0.0 #shoulder
    goals[1] = 0.0 #elbow
    goals[2] = 0.0 #left_F
    goals[3] = 0.0 #left_B
    goals[4] = 0.0 #right_F
    goals[5] = 0.0 #right_B
    goals[6] = drum_value_g #maintains the drum goal through each loop
    
    #Reads the input from the Joystick controller
    if (joystick_count >= 1):  
        goals = JoystickInput.Joystick(goals)
        #we could add a loop here for more controlers.... maybe....

    #Reads the input from the Keyboard
    if (True):
        goals = KeyboardInput.Keyboard(goals)

    #Unpacks the goal values
    shoulder_value_g = goals[0]
    elbow_value_g    = goals[1]
    left_F_value_g   = goals[2]
    left_B_value_g   = goals[3]
    right_F_value_g  = goals[4]
    right_B_value_g  = goals[5]
    drum_value_g     = goals[6]

    #sets actual to be the goal 
    shoulder_value_a = shoulder_value_g #doesn't reqire any more logic
    elbow_value_a = elbow_value_g #doesn't reqire any more logic
    drum_value_a = drum_value_g #rapming logic applied in JoystickInput & KeyboardInput

#Changes the actual motor values to be closer to the goal------------------

#Left motor:
    #Front:
    #if speed change is > than 'MAX_DELTA_W'...
    if(abs(left_F_value_a-left_F_value_g) >= CF.MAX_DELTA_W):
        if(left_F_value_a < left_F_value_g): #if negative delta
            left_F_value_a += CF.MAX_DELTA_W
        elif(left_F_value_a > left_F_value_g): #if positive delta
            left_F_value_a -= CF.MAX_DELTA_W
    else: #if speed change is < than 'MAX_DELTA_W'...
        left_F_value_a = left_F_value_g
    
    #Back:
    #if speed change is > than 'delta_speed'...
    if(abs(left_B_value_a-left_B_value_g) >= CF.MAX_DELTA_W):
        if(left_B_value_a < left_B_value_g):#if negative delta
            left_B_value_a += CF.MAX_DELTA_W
        elif(left_B_value_a > left_B_value_g): #if positive delta
            left_B_value_a -= CF.MAX_DELTA_W
    else: #if speed change is < than 'delta_speed'...
        left_B_value_a = left_B_value_g
    
#Right motor:
    #Front:
    #if speed change is > than 'delta_speed'...
    if(abs(right_F_value_a-right_F_value_g) >= CF.MAX_DELTA_W):
        if(right_F_value_a < right_F_value_g): #if negative delta
            right_F_value_a += CF.MAX_DELTA_W
        elif(right_F_value_a > right_F_value_g): #if positive delta
            right_F_value_a -= CF.MAX_DELTA_W
    else: #if speed change is < than 'delta_speed'...
        right_F_value_a = right_F_value_g
    
    #Back:
    #if speed change is > than 'delta_speed'...
    if(abs(right_B_value_a-right_B_value_g) >= CF.MAX_DELTA_W):
        if(right_B_value_a < right_B_value_g):#if negative delta
            right_B_value_a += CF.MAX_DELTA_W
        elif(right_B_value_a > right_B_value_g):#if positive delta
            right_B_value_a -= CF.MAX_DELTA_W
    else: #if speed change is < than 'delta_speed'...
        right_B_value_a = right_B_value_g

#ESTOPS--------------------------------------------------------------------
    if(CF.FULL_ESTOP): #Triangle/Y (Esc) button
        shoulder_value_a = 0
        elbow_value_a = 0
        left_F_value_a = 0
        left_B_value_a = 0
        right_F_value_a = 0
        right_B_value_a = 0
        drum_value_a = 0
        drum_value_g = 0
    if(CF.DRIVE_ESTOP): #Start (~) button
        left_F_value_a = 0
        left_B_value_a = 0
        right_F_value_a = 0
        right_B_value_a = 0

#Display-------------------------------------------------------------------

    #Displays the Robots motor status
    Display.Display(shoulder_value_a,
                    elbow_value_a,
                    left_F_value_a,
                    left_B_value_a,
                    right_F_value_a,
                    right_B_value_a,
                    drum_value_a)

#Sends the messages to the Ardunio-----------------------------------------

    if(Arduino):
        if(CF.DEBUG_ESTOP): #Select button
            c.send("left_F",int(0)) 
            c.send("left_B",int(0))
            c.send("right_F",int(0))
            c.send("right_B",int(0))
            c.send("shoulder",int(0))
            c.send("elbow",int(0))
            c.send("drum",int(0))
            c.send("FULL_ESTOP",int(CF.FULL_ESTOP))
            c.send("DRIVE_ESTOP",int(CF.DRIVE_ESTOP))
            c.send("DEBUG_ESTOP",int(CF.DEBUG_ESTOP))
        else:
            c.send("left_F",int(left_F_value_a)) 
            c.send("left_B",int(-left_B_value_a)) #Note: Back values are negative to filp polatity
            c.send("right_F",int(right_F_value_a)) 
            c.send("right_B",int(-right_B_value_a))
            c.send("shoulder",int(shoulder_value_a))
            c.send("elbow",int(elbow_value_a))
            c.send("drum",int(drum_value_a))
            c.send("FULL_ESTOP",int(CF.FULL_ESTOP))
            c.send("DRIVE_ESTOP",int(CF.DRIVE_ESTOP))
            c.send("DEBUG_ESTOP",int(CF.DEBUG_ESTOP))

#Print-screen--------------------------------------------------------------

    if(Arduino):
        msg_readout +=1
        if(False):
            msg = c.receive()
            print(msg)
        if (msg_readout==msg_interval):
            msg_readout = 0
            print("10 frames")
    
#ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT-----------------------------
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
#END-OF-LOOP---------------------------------------------------------------
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
