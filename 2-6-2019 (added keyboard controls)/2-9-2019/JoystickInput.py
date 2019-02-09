import pygame
import CF

def Joystick(goals):

    #initializes the ith Joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    #initalize motor "goal" variables
    shoulder_value_g = goals[0]
    elbow_value_g    = goals[1]
    left_F_value_g   = goals[2]
    left_B_value_g   = goals[3]
    right_F_value_g  = goals[4]
    right_B_value_g  = goals[5]
    drum_value_g     = goals[6]

    #Arm actuators-------------------------------------------------------------

    #Shoulder:
    shoulder_value_g = 0
    if (joystick.get_axis(5) >= 0.9):
        shoulder_value_g += 1000
    if (joystick.get_button(5) == 1):
        shoulder_value_g -= 1000
            
    #Elbow:
    elbow_value_g = 0
    if (joystick.get_axis(2) >= 0.9):
        elbow_value_g += 1000
    if (joystick.get_button(4) == 1):
        elbow_value_g -= 1000

#Sets the goal for all the motor values------------------------------------
               
    #Thumbsticks:
    left_F_value_g = -joystick.get_axis(1)*CF.MAX_SPEED_W
    left_B_value_g = -joystick.get_axis(1)*CF.MAX_SPEED_W
    right_F_value_g = -joystick.get_axis(4)*CF.MAX_SPEED_W
    right_B_value_g = -joystick.get_axis(4)*CF.MAX_SPEED_W

    #Dpad-Control
    hat = joystick.get_hat(0)
    #Left
    if(hat[0] == -1):
        left_F_value_g  = -CF.MAX_DPAD_W
        left_B_value_g  = -CF.MAX_DPAD_W
        right_F_value_g = CF.MAX_DPAD_W
        right_B_value_g = CF.MAX_DPAD_W
    #Right
    elif(hat[0] == 1):
        left_F_value_g  = CF.MAX_DPAD_W
        left_B_value_g  = CF.MAX_DPAD_W
        right_F_value_g = -CF.MAX_DPAD_W
        right_B_value_g = -CF.MAX_DPAD_W
    #forward
    if(hat[1] == 1):
        left_F_value_g  = CF.MAX_DPAD_W
        left_B_value_g  = CF.MAX_DPAD_W
        right_F_value_g = CF.MAX_DPAD_W
        right_B_value_g = CF.MAX_DPAD_W
    #Backwards
    elif(hat[1] == -1):
        left_F_value_g  = -CF.MAX_DPAD_W
        left_B_value_g  = -CF.MAX_DPAD_W
        right_F_value_g = -CF.MAX_DPAD_W
        right_B_value_g = -CF.MAX_DPAD_W
    #Save olf value
    CF.old_hat_0 = hat

#Drum----------------------------------------------------------------------

    #drum:
    #forward (dig)
    if(CF.old_joystick_1 == joystick.get_button(1)): #if button is the same...
        pass #do nothing
    elif(joystick.get_button(1) == 1 and drum_value_g < CF.MAX_SPEED_D):
        drum_value_g += CF.MAX_DELTA_D
    CF.old_joystick_1 = joystick.get_button(1) #updates old value
    #reverse (dump)
    if(CF.old_joystick_2 == joystick.get_button(2)): #if button is the same...
        pass #do nothing
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

#Togalable ESTOPs----------------------------------------------------------

#DEBUG_ESTOP for everything
    if(CF.old_joystick_6 == joystick.get_button(6)): #Select button
        CF.DEBUG_ESTOP=CF.DEBUG_ESTOP
    elif(joystick.get_button(6) == 1):
        if(CF.DEBUG_ESTOP==1):
            CF.DEBUG_ESTOP=0
        else:
            CF.DEBUG_ESTOP=1
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

#--------------------------------------------------------------------------

    goals = [shoulder_value_g,
             elbow_value_g,
             left_F_value_g,
             left_B_value_g,
             right_F_value_g,
             right_B_value_g,
             drum_value_g]
    
    return goals
    
