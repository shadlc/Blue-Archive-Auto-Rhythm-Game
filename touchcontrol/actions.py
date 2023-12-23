from touchcontrol.controls import *


def tap(coords: tuple[int, int]):
    """
    Emulates a single tap on the touch screen.
    :param coords: Tuple of screen coordinates where tap should occur  (x,y)
    :return: None
    """

    finger_down(coords)   # Simulate finger touching screen
    finger_up()   # Simulate finger leaving the screen


def swipe(start_coords: tuple[int, int], end_coords: tuple[int, int], num_steps=10):
    """
    Method to emulate a linear swiping motion on touch screen.
    Example: Panning a map.
    :param start_coords: Tuple of screen coordinates where swiping should start (x, y)
    :param end_coords: Tuple of screen coordinates where swiping should end (x, y)
    :param num_steps: Number of steps used for linear interpolation between start and end. Use higher number for smoother movement.
    :return: None
    """

    finger_down(start_coords)

    x_step = int((end_coords[0] - start_coords[0]) / num_steps)
    y_step = int((end_coords[1] - end_coords[0]) / num_steps)
    offset = (x_step, y_step)
    for i in range(num_steps):
        move_finger(offset)
        sleep(0.01)

    # Pull Up
    finger_up()


def spread(start_f1: tuple[int, int], end_f1: tuple[int, int],
           start_f2: tuple[int, int], end_f2: tuple[int, int], num_steps=10):
    """
    Method emulating a spreading multitouch gesture by emulating two fingers swiping across the screen
    Example: Two fingers performing an opening or closing gesture to zoom in/out of an image.
    :param start_f1: Screen coordinates of where the first finger starts swiping (x,y)
    :param end_f1: Screen coordinates of where the first finger ends swiping (x,y)
    :param start_f2: Screen coordinates of where the second finger starts swiping (x,y)
    :param end_f2: Screen coordinaets of where the second finger ends swiping (x,y)
    :param num_steps: Number of steps used for linear interpolation between start and end. Use higher number for smoother movement.
    :return: None
    """

    # Press Down
    two_fingers_down(start_f1, start_f2)

    x1_step = int((end_f1[0] - start_f1[0]) / num_steps)
    y1_step = int((end_f1[1] - start_f1[1]) / num_steps)
    finger_1_offset = (x1_step, y1_step)

    x2_step = int((end_f2[0] - start_f2[0]) / num_steps)
    y2_step = int((end_f2[1] - start_f2[1]) / num_steps)
    finger_2_offset = (x2_step, y2_step)

    for i in range(num_steps):
        move_two_fingers(finger_1_offset, finger_2_offset)
        sleep(0.01)

    # Pull Up
    two_fingers_up()
