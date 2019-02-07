import pygame
import PyCmdMessenger
import TextPrint
import CF
import Display

arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyACM0",baud_rate=9600)

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

c = PyCmdMessenger.CmdMessenger(arduino,commands)

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

#other variables
#Display
display_joysticks = 0 #(True/False)

#msg read out
msg_readout = 0

#SET_UP--------------------------------------------------------------------

pygame.init()

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint.TextPrint()

#Main Program Loop---------------------------------------------------------

while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

#Arm actuators-------------------------------------------------------------

    #Shoulder:
        shoulder_value_g = 0
        if (joystick.get_axis(5) >= 0.9):
            shoulder_value_g += 1000
        if (joystick.get_button(5) == 1):
            shoulder_value_g -= 1000
        shoulder_value_a = shoulder_value_g
            
    #Elbow:
        elbow_value_g = 0
        if (joystick.get_axis(2) >= 0.9):
            elbow_value_g += 1000
        if (joystick.get_button(4) == 1):
            elbow_value_g -= 1000
        elbow_value_a = elbow_value_g

#Sets the goal for all the motor values------------------------------------

    #Dpad-Control-1
        if(joystick.get_hat(0)==(0,0)): #if Dpad isn't pressed
            left_F_value_g = 0
            left_B_value_g = 0
            right_F_value_g = 0
            right_B_value_g = 0
               
    #Thumbsticks:
        left_F_value_g = joystick.get_axis(1)*CF.MAX_SPEED_W
        left_B_value_g = joystick.get_axis(1)*CF.MAX_SPEED_W
        right_F_value_g = joystick.get_axis(4)*CF.MAX_SPEED_W
        right_B_value_g = joystick.get_axis(4)*CF.MAX_SPEED_W

    #Dpad-Control-2
        hat = joystick.get_hat(0)
        #Left
        if(hat[0] == 1):
            left_F_value_g = -CF.MAX_DPAD_W
            left_B_value_g = -CF.MAX_DPAD_W
            right_F_value_g = CF.MAX_DPAD_W
            right_B_value_g = CF.MAX_DPAD_W
        #Right
        elif(hat[0] == -1):
            left_F_value_g = CF.MAX_DPAD_W
            left_B_value_g = CF.MAX_DPAD_W
            right_F_value_g = -CF.MAX_DPAD_W
            right_B_value_g = -CF.MAX_DPAD_W
        #forward
        if(hat[1] == 1):
            left_F_value_g = -CF.MAX_DPAD_W
            left_B_value_g = -CF.MAX_DPAD_W
            right_F_value_g = -CF.MAX_DPAD_W
            right_B_value_g = -CF.MAX_DPAD_W
        #Backwards
        elif(hat[1] == -1):
            left_F_value_g = CF.MAX_DPAD_W
            left_B_value_g = CF.MAX_DPAD_W
            right_F_value_g = CF.MAX_DPAD_W
            right_B_value_g = CF.MAX_DPAD_W
        #Save olf value
        CF.old_hat_0 = hat

#Drum----------------------------------------------------------------------

    #drum:
        #forward (dig)
        if(CF.old_joystick_1 == joystick.get_button(1)): #if button is the same...
            drum_value_g = drum_value_g #do nothing
        elif(joystick.get_button(1) == 1 and drum_value_g < CF.MAX_SPEED_D):
            drum_value_g += CF.MAX_DELTA_D
        CF.old_joystick_1 = joystick.get_button(1) #updates old value
        #reverse (dump)
        if(CF.old_joystick_2 == joystick.get_button(2)): #if button is the same...
            drum_value_g = drum_value_g #do nothing
        elif(joystick.get_button(2) == 1 and drum_value_g > -CF.MAX_SPEED_D):
            drum_value_g -= CF.MAX_DELTA_D
        CF.old_joystick_2 = joystick.get_button(2) #updates old value
        #Estop for just the drum (with ramp down)
        if(joystick.get_button(0) == 1): #X button
            if(drum_value_g > CF.MAX_STOP_D):
                drum_value_g -= CF.MAX_STOP_D
            elif(drum_value_g < -CF.MAX_STOP_D):
                drum_value_g += CF.MAX_STOP_D 
            else:
                drum_value_g = 0

        drum_value_a = drum_value_g

#TEMP KEYBOARD-------------------------------------------------------------
    #Gets array of keyboard button presses
        Key_board = pygame.key.get_pressed()

    #Driving
        #Forward
        if(Key_board[pygame.K_w]):
            left_F_value_g = -CF.MAX_DPAD_W
            left_B_value_g = -CF.MAX_DPAD_W
            right_F_value_g = -CF.MAX_DPAD_W
            right_B_value_g = -CF.MAX_DPAD_W
        #Backward
        elif(Key_board[pygame.K_s]):
            left_F_value_g = CF.MAX_DPAD_W
            left_B_value_g = CF.MAX_DPAD_W
            right_F_value_g = CF.MAX_DPAD_W
            right_B_value_g = CF.MAX_DPAD_W
        #Left
        elif(Key_board[pygame.K_a]):
            left_F_value_g = CF.MAX_DPAD_W
            left_B_value_g = CF.MAX_DPAD_W
            right_F_value_g = -CF.MAX_DPAD_W
            right_B_value_g = -CF.MAX_DPAD_W
        #Right
        elif(Key_board[pygame.K_d]):
            left_F_value_g = -CF.MAX_DPAD_W
            left_B_value_g = -CF.MAX_DPAD_W
            right_F_value_g = CF.MAX_DPAD_W
            right_B_value_g = CF.MAX_DPAD_W

    #Shoulder:
        if (Key_board[pygame.K_KP4]):
            shoulder_value_g += 1000
        if (Key_board[pygame.K_KP1]):
            shoulder_value_g -= 1000
        shoulder_value_a = shoulder_value_g
            
    #Elbow:
        if (Key_board[pygame.K_KP5]):
            elbow_value_g += 1000
        if (Key_board[pygame.K_KP2]):
            elbow_value_g -= 1000
        elbow_value_a = elbow_value_g

    #drum:
        #forward (dig)
        if(CF.old_K_KP6 == Key_board[pygame.K_KP6]): #if button is the same...
            drum_value_g = drum_value_g #do nothing
        elif(Key_board[pygame.K_KP6] and drum_value_g < CF.MAX_SPEED_D):
            drum_value_g += CF.MAX_DELTA_D
        CF.old_K_KP6 = Key_board[pygame.K_KP6] #updates old value
        #reverse (dump)
        if(CF.old_K_KP3 == Key_board[pygame.K_KP3]): #if button is the same...
            drum_value_g = drum_value_g #do nothing
        elif(Key_board[pygame.K_KP3] and drum_value_g > -CF.MAX_SPEED_D):
            drum_value_g -= CF.MAX_DELTA_D
        CF.old_K_KP3 = Key_board[pygame.K_KP3] #updates old value
        #Estop for just the drum (with ramp down)
        if(Key_board[pygame.K_KP0]):
            if(drum_value_g > CF.MAX_STOP_D):
                drum_value_g -= CF.MAX_STOP_D
            elif(drum_value_g < -CF.MAX_STOP_D):
                drum_value_g += CF.MAX_STOP_D 
            else:
                drum_value_g = 0

        drum_value_a = drum_value_g

    #DEBUG_ESTOP for everything
        if(CF.old_K_1 == Key_board[pygame.K_1]): #Select button
            CF.DEBUG_ESTOP=CF.DEBUG_ESTOP
        elif(Key_board[pygame.K_1]):
            if(CF.DEBUG_ESTOP==1):
                CF.DEBUG_ESTOP=0
                display_joysticks=0
            else:
                CF.DEBUG_ESTOP=1
                display_joysticks=1
        CF.old_K_1 = Key_board[pygame.K_1] #updates old value
    #FULL_ESTOP for everything
        if(Key_board[pygame.K_SPACE]):
            CF.FULL_ESTOP=1
            CF.DRIVE_ESTOP=1
        if(CF.old_K_ESCAPE == Key_board[pygame.K_ESCAPE]): #Triangle button
            CF.FULL_ESTOP=CF.FULL_ESTOP
        elif(Key_board[pygame.K_ESCAPE] == 1):
            if(CF.FULL_ESTOP==1):
                CF.FULL_ESTOP=0
            else:
                CF.FULL_ESTOP=1
        CF.old_K_ESCAPE = Key_board[pygame.K_ESCAPE] #updates old value
    #Drive_ESTOP for everything
        if(CF.old_K_BACKQUOTE == Key_board[pygame.K_BACKQUOTE]): #Triangle button
            CF.DRIVE_ESTOP=CF.DRIVE_ESTOP
        elif(Key_board[pygame.K_BACKQUOTE] == 1):
            if(CF.DRIVE_ESTOP==1):
                CF.DRIVE_ESTOP=0
            else:
                CF.DRIVE_ESTOP=1
        CF.old_K_BACKQUOTE = Key_board[pygame.K_BACKQUOTE] #updates old value
            



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


#Togalable ESTOPs----------------------------------------------------------

    #DEBUG_ESTOP for everything
        if(CF.old_joystick_6 == joystick.get_button(6)): #Select button
            CF.DEBUG_ESTOP=CF.DEBUG_ESTOP
        elif(joystick.get_button(6) == 1):
            if(CF.DEBUG_ESTOP==1):
                CF.DEBUG_ESTOP=0
                display_joysticks=0
            else:
                CF.DEBUG_ESTOP=1
                display_joysticks=1
        CF.old_joystick_6 = joystick.get_button(6) #updates old value

    #FULL_ESTOP for everything
        if(CF.old_joystick_3 == joystick.get_button(3)): #Triangle button
            CF.FULL_ESTOP=CF.FULL_ESTOP
        elif(joystick.get_button(3) == 1):
            if(CF.FULL_ESTOP==1):
                CF.FULL_ESTOP=0
            else:
                CF.FULL_ESTOP=1
        CF.old_joystick_3 = joystick.get_button(3) #updates old value
        if(CF.FULL_ESTOP): #Triangle button
            shoulder_value_a = 0
            elbow_value_a = 0
            left_F_value_a = 0
            left_B_value_a = 0
            right_F_value_a = 0
            right_B_value_a = 0
            drum_value_a = 0
            drum_value_g = 0

    #DRIVE_ESTOP for everything
        if(CF.old_joystick_7 == joystick.get_button(7)): #Start button
            CF.DRIVE_ESTOP=CF.DRIVE_ESTOP
        elif(joystick.get_button(7) == 1):
            if(CF.DRIVE_ESTOP==1):
                CF.DRIVE_ESTOP=0
            else:
                CF.DRIVE_ESTOP=1
        CF.old_joystick_7 = joystick.get_button(7) #updates old value
        if(CF.DRIVE_ESTOP): #Start button
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
                        drum_value_a,
                        i,
                        display_joysticks)

#Sends the messages to the Ardunio-----------------------------------------

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
        c.send("left_F",int(-left_F_value_a)) 
        c.send("left_B",int(left_B_value_a))
        c.send("right_F",int(-right_F_value_a)) #Note: front values are negative to filp polatity
        c.send("right_B",int(right_B_value_a))
        c.send("shoulder",int(shoulder_value_a))
        c.send("elbow",int(elbow_value_a))
        c.send("drum",int(drum_value_a))
        c.send("FULL_ESTOP",int(CF.FULL_ESTOP))
        c.send("DRIVE_ESTOP",int(CF.DRIVE_ESTOP))
        c.send("DEBUG_ESTOP",int(CF.DEBUG_ESTOP))

#--------------------------------------------------------------------------

    #Recive message from ardunio
    msg = c.receive()

    msg_readout +=1
    if (msg_readout==10):
        msg_readout = 0
        print(msg)
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
#--------------------------------------------------------------------------
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
