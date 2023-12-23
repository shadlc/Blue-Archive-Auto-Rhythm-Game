from ctypes import *
from ctypes.wintypes import *

from time import sleep

# Constants

# For touchMask
TOUCH_MASK_NONE = 0x00000000  # Default
TOUCH_MASK_CONTACTAREA = 0x00000001
TOUCH_MASK_ORIENTATION = 0x00000002
TOUCH_MASK_PRESSURE = 0x00000004
TOUCH_MASK_ALL = 0x00000007

# For touchFlag
TOUCH_FLAG_NONE = 0x00000000

# For pointerType
PT_POINTER = 0x00000001  # All
PT_TOUCH = 0x00000002
PT_PEN = 0x00000003
PT_MOUSE = 0x00000004

# For pointerFlags
POINTER_FLAG_NONE = 0x00000000  # Default
POINTER_FLAG_NEW = 0x00000001
POINTER_FLAG_INRANGE = 0x00000002
POINTER_FLAG_INCONTACT = 0x00000004
POINTER_FLAG_FIRSTBUTTON = 0x00000010
POINTER_FLAG_SECONDBUTTON = 0x00000020
POINTER_FLAG_THIRDBUTTON = 0x00000040
POINTER_FLAG_FOURTHBUTTON = 0x00000080
POINTER_FLAG_FIFTHBUTTON = 0x00000100
POINTER_FLAG_PRIMARY = 0x00002000
POINTER_FLAG_CONFIDENCE = 0x00004000
POINTER_FLAG_CANCELED = 0x00008000
POINTER_FLAG_DOWN = 0x00010000
POINTER_FLAG_UPDATE = 0x00020000
POINTER_FLAG_UP = 0x00040000
POINTER_FLAG_WHEEL = 0x00080000
POINTER_FLAG_HWHEEL = 0x00100000
POINTER_FLAG_CAPTURECHANGED = 0x00200000


class POINTER_INFO(Structure):
    _fields_=[("pointerType",c_uint32),
              ("pointerId",c_uint32),
              ("frameId",c_uint32),
              ("pointerFlags",c_int),
              ("sourceDevice",HANDLE),
              ("hwndTarget",HWND),
              ("ptPixelLocation",POINT),
              ("ptHimetricLocation",POINT),
              ("ptPixelLocationRaw",POINT),
              ("ptHimetricLocationRaw",POINT),
              ("dwTime",DWORD),
              ("historyCount",c_uint32),
              ("inputData",c_int32),
              ("dwKeyStates",DWORD),
              ("PerformanceCount",c_uint64),
              ("ButtonChangeType",c_int)
              ]

class POINTER_TOUCH_INFO(Structure):
    _fields_=[("pointerInfo",POINTER_INFO),
              ("touchFlags",c_int),
              ("touchMask",c_int),
              ("rcContact", RECT),
              ("rcContactRaw",RECT),
              ("orientation", c_uint32),
              ("pressure", c_uint32)]


ntouch = 2

touchInfo = (POINTER_TOUCH_INFO * ntouch)()

touchInfo[0].pointerInfo.pointerType = PT_TOUCH
touchInfo[0].pointerInfo.pointerId = 0
touchInfo[0].pointerInfo.ptPixelLocation.y = 1000
touchInfo[0].pointerInfo.ptPixelLocation.x = 500

touchInfo[0].touchFlags = TOUCH_FLAG_NONE
touchInfo[0].touchMask = TOUCH_MASK_ALL
touchInfo[0].orientation = 90
touchInfo[0].pressure = 32000
touchInfo[0].rcContact.top = touchInfo[0].pointerInfo.ptPixelLocation.y - 2
touchInfo[0].rcContact.bottom = touchInfo[0].pointerInfo.ptPixelLocation.y + 2
touchInfo[0].rcContact.left = touchInfo[0].pointerInfo.ptPixelLocation.x - 2
touchInfo[0].rcContact.right = touchInfo[0].pointerInfo.ptPixelLocation.x + 2

touchInfo[1].pointerInfo.pointerType = PT_TOUCH
touchInfo[1].pointerInfo.pointerId = 1
touchInfo[1].pointerInfo.ptPixelLocation.y = 900
touchInfo[1].pointerInfo.ptPixelLocation.x = 300

touchInfo[1].touchFlags = TOUCH_FLAG_NONE
touchInfo[1].touchMask = TOUCH_MASK_ALL
touchInfo[1].orientation = 90
touchInfo[1].pressure = 32000
touchInfo[1].rcContact.top = touchInfo[1].pointerInfo.ptPixelLocation.y - 2
touchInfo[1].rcContact.bottom = touchInfo[1].pointerInfo.ptPixelLocation.y + 2
touchInfo[1].rcContact.left = touchInfo[1].pointerInfo.ptPixelLocation.x - 2
touchInfo[1].rcContact.right = touchInfo[1].pointerInfo.ptPixelLocation.x + 2

if windll.user32.InitializeTouchInjection(ntouch, 2) is False:
    print("Initialized Touch Injection Error")
else:
    print("initilaization successful")


def inject_single(idx: int = 0):
    """
    Method to inject a single touch pointer into the system.
    Injected pointer is touchInfo[0]
    :param idx: Index which pointer in touchInfo should be injected, defaults to 0
    :return: None
    """
    if windll.user32.InjectTouchInput(1, byref(touchInfo[idx])) is False:
        raise Exception("Touch Injection went wrong")


def inject_double():
    """
    Method to inject a double touch pointer into the systsem.
    Injected pointers are tuochInfo
    :return: None
    """
    if windll.user32.InjectTouchInput(ntouch, byref(touchInfo)) is False:
        raise Exception("Touch Injection went wrong")


def pointer_make_contact_single(coords: tuple[int, int], idx: int = 0):
    """
    Update pointer flags to indicate that a pointer has made contact with the screen at position defined by coords.
    Simulates a finger touching the screen
    :param coords: Tuple of coordinates on screen where contact is made: (x, y)
    :param idx: Index which pointer in touchInfo should simulate contact, defaults to 0
    :return: None
    """

    touchInfo[idx].pointerInfo.ptPixelLocation.x = coords[0]
    touchInfo[idx].pointerInfo.ptPixelLocation.y = coords[1]
    touchInfo[idx].pointerInfo.pointerFlags = (POINTER_FLAG_DOWN | POINTER_FLAG_INRANGE | POINTER_FLAG_INCONTACT)


def pointer_make_contact_double(coords: tuple[tuple[int, int], tuple[int, int]]):
    """
    Update poitner flags to indicate they have made contact with the screen.
    Simulates multiple fingers touching the screen at position of coords
    :param coords: Tuple of Tuple of coordinates. Length of outer touple must be teh same as length of touchInfo. ( (x1, y1), (x2, y2) )
    :return: None
    """
    assert len(coords) == len(touchInfo)
    for coord_pair, idx in zip(coords, range(len(touchInfo))):
        pointer_make_contact_single(coord_pair, idx)


def pointer_update_single(coords: tuple[int, int], idx: int = 0):
    """
    Update pointer flags and coordinates to indcate a pointer has changed psoition on screen.
    Simulates a finger moving on screen.
    :param coords: Screen coords, to which pointer should move
    :param idx: Index which pointer in touchInfo should update, defaults to 0
    :return: None
    """
    touchInfo[idx].pointerInfo.ptPixelLocation.x = coords[0]
    touchInfo[idx].pointerInfo.ptPixelLocation.y = coords[1]
    touchInfo[idx].pointerInfo.pointerFlags = (POINTER_FLAG_INRANGE | POINTER_FLAG_INCONTACT | POINTER_FLAG_UPDATE)


def pointer_udpate_single_relative(coord_offset: tuple[int, int], idx: int = 0):
    coords = (touchInfo[idx].pointerInfo.ptPixelLocation.x + coord_offset[0],
              touchInfo[idx].pointerInfo.ptPixelLocation.y + coord_offset[1])
    pointer_update_single(coords, idx)


def pointer_update_double(coords: tuple[tuple[int, int], tuple[int, int]]):
    """
    Update pointer flags to indicate their position has chagned on screen.
    :param coords:
    :return:
    """
    for coord_pair, idx in zip(coords, range(len(touchInfo))):
        pointer_update_single(coord_pair, idx)


def pointer_update_double_relative(offsets: tuple[tuple[int, int], tuple[int, int]]):
    for offset, idx in zip(offsets, range(len(touchInfo))):
        pointer_udpate_single_relative(offset, idx)


def pointer_leave_single(idx: int = 0):
    """
    Update pointer flags to indicate a pointer has left the screen.
    Simulates a finger taken off the touch screen
    :param idx: Index which pointer in touchInfo should leave, defaults to 0
    :return: None
    """
    touchInfo[idx].pointerInfo.pointerFlags = POINTER_FLAG_UP


def pointer_leave_double():
    """
    Update pointer flags to indicate they have left the screen.
    :return: None
    """
    for idx in range(len(touchInfo)):
        pointer_leave_single(idx)
