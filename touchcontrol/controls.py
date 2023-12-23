from touchcontrol._wrapper import *


def finger_down(coords: tuple[int, int]):
    """
    Emulate putting a finger down onto the screen. Call finger_up() to simulate the finger leaving the screen.
    :param coords: Tuple containing screen coordinates wehre finger is placed on screen: (x, y)
    :return: None
    """

    pointer_make_contact_single(coords)
    inject_single()


def two_fingers_down(finger1_coords: tuple[int, int], finger2_coords: tuple[int, int]):
    """
    Emulates putting two fingers onto the screen. Call two_fingers_up to simulate both fingers leaving the screen.
    :param finger1_coords: Tuple containing screen coordinates wehre first finger is placed on screen: (x, y)
    :param finger2_coords: Tuple containing screen coordinates wehre second finger is placed on screen: (x, y)
    :return: None
    """
    coords = (finger1_coords, finger2_coords)
    pointer_make_contact_double(coords)
    inject_double()


def finger_up():
    """
    Method to simualte taking the finger off the screen. finger_down() must have been called before
    :return: None
    """
    pointer_leave_single()
    inject_single()


def two_fingers_up():
    """
    Method to simulate taking both fingers off the screen. two_fingers_down() must have been called before.
    :return:
    """
    pointer_leave_double()
    inject_double()


def move_finger(coord_offset: tuple[int, int]):
    """
    Method to simulate a finger sliding across the screen. finger_down() must have been called before.
    :param coord_offset: Tuple indicating finger movement in pixels, relative to curernt position, e.g. (dx, dy)
    :return: None
    """
    pointer_udpate_single_relative(coord_offset)
    inject_single()


def move_two_fingers(coord_offset_finger_1: tuple[int, int], corod_offset_finger_2: tuple[int, int]):
    """
    Method to simulate two fingers sliding across the screen. two_fingers_down() must have been called before.
    :param coord_offset_finger_1: Tuple indicating finger-1 movement in pixels, relative to curernt position, e.g. (dx, dy)
    :param corod_offset_finger_2: Tuple indicating finger-2 movement in pixels, relative to curernt position, e.g. (dx, dy)
    :return: None
    """
    offsets = (coord_offset_finger_1, corod_offset_finger_2)
    pointer_update_double_relative(offsets)
    inject_double()
