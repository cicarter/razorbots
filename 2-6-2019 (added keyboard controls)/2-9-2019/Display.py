import pygame
import CF
import TextPrint

def Display(shoulder_value,
            elbow_value,
            left_F_value,
            left_B_value,
            right_F_value,
            right_B_value,
            drum_value):

    # Set the width and height of the screen [width,height]
    if(CF.DEBUG_ESTOP):
        screen = pygame.display.set_mode(CF.SIZE2)
    else:
        screen = pygame.display.set_mode(CF.SIZE1)

    #Joystick Prep
    #Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    if (joystick_count > 0):
        joystick = pygame.joystick.Joystick(0)
    
    # Get ready to print
    textPrint = TextPrint.TextPrint()

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(CF.WHITE)
    textPrint.reset()


    if(CF.DEBUG_ESTOP):
##        textPrint.print(screen, "Number of joysticks: {}".format(1) )
##        textPrint.indent()
##        #Prints out Controller values
##        textPrint.print(screen, "Joystick {}".format(1))
##        textPrint.indent()

        if (joystick_count == 0):
            textPrint.print(screen, "NO JOYSTICK!")
        elif (joystick_count > 0):
            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.print(screen, "Joystick name: {}".format(name))
            
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.print(screen, "Number of Axis: {}".format(axes))
            textPrint.indent()
            for i in range(axes):
                axis = joystick.get_axis(i)
                textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))

            #Buttons
            textPrint.unindent()
            buttons = joystick.get_numbuttons()
            textPrint.print(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()
            for i in range( buttons ):
                button = joystick.get_button(i)
                textPrint.print(screen, "Button {:>2} value: {}".format(i,button))
            textPrint.unindent()
                
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print(screen, "Number of hats: {}".format(hats))
            textPrint.indent()
            for i in range( hats ):
                hat = joystick.get_hat(i)
                textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
                textPrint.unindent()
                textPrint.print(screen, " ")

        
        #E-stop satus
    if (CF.DEBUG_ESTOP):
        textPrint.print_red(screen, "Debugging: TRUE")
    if (CF.FULL_ESTOP):
        textPrint.print_red(screen, "FULL_ESTOP: TRUE")
    else:
        textPrint.print_green(screen, "FULL_ESTOP: FALSE")
    if (CF.DRIVE_ESTOP):
        textPrint.print_red(screen, "DRIVE_ESTOP: TRUE")
    else:
        textPrint.print_green(screen, "DRIVE_ESTOP: FALSE")
        
    #motor status
    textPrint.print(screen, "Drive Train:")
    textPrint.indent()
    textPrint.print(screen, "Left:")
    textPrint.indent()
    textPrint.print(screen, "Front: {}".format(left_F_value))
    textPrint.print(screen, "Back:  {}".format(left_B_value))
    textPrint.unindent()
    textPrint.print(screen, "Right:")
    textPrint.indent()
    textPrint.print(screen, "Front: {}".format(right_F_value))
    textPrint.print(screen, "Back:  {}".format(right_B_value))
    textPrint.unindent()
    textPrint.unindent()

    #Acctuator status
    textPrint.print(screen, "Arm:")
    textPrint.indent()
    textPrint.print(screen, "shoulder: {}".format(shoulder_value))
    textPrint.print(screen, "elbow:     {}".format(elbow_value))
    textPrint.unindent()
    #Drum status
    textPrint.print(screen, "Drum:")
    textPrint.indent()
    textPrint.print(screen, "Speed: {}".format(drum_value))
    textPrint.unindent()
