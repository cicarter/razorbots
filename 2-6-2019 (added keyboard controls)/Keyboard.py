import CF
import pygame

def keyBoardCmds(shoulder_value_g,
                    elbow_value_g,
                    left_F_value_g,
                    left_B_value_g,
                    right_F_value_g,
                    right_B_value_g,
                    drum_value_g):

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
        pass
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
    return left_F_value_g, left_B_value_g, right_F_value_g, right_B_value_g
