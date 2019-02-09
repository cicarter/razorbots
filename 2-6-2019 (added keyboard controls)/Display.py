import CF
import TextPrint
import pygame

def Display(shoulder_value,
            elbow_value,
            left_F_value,
            left_B_value,
            right_F_value,
            right_B_value,
            drum_value,
            joystick_num,
            display_joysticks):

    display_width = 300
    display_height = 650
    # Set the width and height of the screen [width,height]
    pygame.init()
    if(not display_joysticks):
        screen = pygame.display.set_mode(CF.SIZE2)
    else:
        screen = pygame.display.set_mode((display_width, display_height))

    #Joystick Prep
    # joystick = pygame.joystick.Joystick(joystick_num)
    # #Get count of joysticks
    # joystick_count = pygame.joystick.get_count()

    # Get ready to print
    textPrint = TextPrint.TextPrint()

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(CF.WHITE)
    textPrint.reset()

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
    textPrint.print(screen, "Front: {}".format(-left_F_value))
    textPrint.print(screen, "Back:  {}".format(-left_B_value))
    textPrint.unindent()
    textPrint.print(screen, "Right:")
    textPrint.indent()
    textPrint.print(screen, "Front: {}".format(-right_F_value))
    textPrint.print(screen, "Back:  {}".format(-right_B_value))
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
