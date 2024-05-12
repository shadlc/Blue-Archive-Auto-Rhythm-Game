import math
import mss
import time
import random
import pyautogui
import threading
import touchcontrol as tc
from PIL import Image
from collections import deque
from pygetwindow import Win32Window


# 本项目的核心类
class Clicker():

    def __init__(self, window: Win32Window) -> None:
        """初始化点击器

        Args:
            window (Win32Window, optional): 识别到的窗口
        """        
        self.window_size = [self.height, self.width] = [0, 0]
        self.left = self.right = self.top = self.bottom = 0
        self.window = window
        self.window_size = window.size
        self.height = window.size[1]
        self.width = window.size[0]
        self.left = window.left if window.left > 0 else 0
        self.right = window.right if window.right > 0 else 0
        self.top = window.top if window.top > 0 else 0
        self.bottom = window.bottom if window.bottom > 0 else 0
        
        self.press_count = 0
        self.tolerance = 10                                                 # 颜色识别容差
        self.frame_time = 0.019                                             # 每帧时长

        # 左侧点击按钮颜色列表
        self.left_colors = [
            [9, 30, 61], [12, 41, 70], [14, 53, 79],
            [15, 38, 67],[16, 46, 71],
            [21, 70, 87], [22, 40, 67], [25, 89, 98],
            [26, 79, 91], [30, 58, 82],
            [33, 99, 111], [36, 112, 122], [40, 125, 130],
            [45, 156, 150], [44, 144, 144], [51, 164, 160],
            [51, 177, 166],
            [54, 186, 174], [57, 186, 186], [58, 200, 190],
            [59, 204, 193], [60, 196, 186], [64, 214, 198],
        ]
        # 右侧点击按钮颜色列表
        self.right_colors = [
            [58, 42, 36], [55, 32, 35], [61, 41, 41], [62, 48, 42],
            [72, 52, 35], [73, 60, 41], [63, 40, 34], [89, 65, 30], [89, 52, 19],
            [83, 65, 46], [105, 81, 31], [111, 89, 36],
            [119, 99, 36], [129, 103, 28], [140, 116, 31],
            [152, 125, 18], [162, 132, 26],
            [160, 134, 15], [172, 137, 22], [174, 144, 31],
            [175, 148, 13], [181, 144, 23], [186, 151, 33],
            [190, 162, 23], [201, 166, 21], [202, 167, 33],
            [208, 172, 10], [211, 171, 25], [213, 179, 18], [217, 181, 32],
            [225, 190, 8], [226, 190, 18], [226, 190, 12], [226, 191, 39],
            [226, 190, 28], [231, 200, 27], [235, 199, 15],
            [235, 199, 6], [236, 196, 24],
        ]
        # 两侧按钮颜色列表
        self.both_colors = [
            [204, 119, 214], [202,109,214],
            [196, 105, 207], [179, 95, 198], [171, 95, 190],
            [150, 78, 169], [127, 67, 143], [133, 71, 152],
            [111, 65, 135], [116, 58, 141], [101, 52, 115], [106, 55, 133],
            [93, 47, 132], [79, 35, 116], [66, 29, 113], [61, 33, 110],
            [85, 51, 115], [60, 37, 92], [58, 28, 90], [52, 33, 87],
        ]
        self.click_color = [0, 0, 0]                                        # 点击监测点颜色
        self.slide_color = [0, 0, 0]                                        # 上划监测点颜色
        self.press_color = [0, 0, 0]                                        # 长按监测点颜色

        self.click_detect_point = [0, 0]                                    # 点击检测点坐标
        self.slide_detect_point = [0, 0]                                    # 上划检测点坐标
        self.press_detect_point = [0, 0]                                    # 长按检测点坐标
        self.left_point = [0, 0]                                            # 左侧点击点坐标
        self.right_point = [0, 0]                                           # 右侧点击点坐标
        self.pat_point = [0, 0]                                             # 摸头坐标(测试用)
        self.initPoint()

        self.action_position = None                                         # 触控位置
        self.action_type = None                                             # 触控类型
        self.past_action = deque([[None, None] * 3], maxlen=3)              # 过去的触控方式

    def initPoint(self) -> None:
        """
        初始化检测点坐标
        因为是按比例获取, 因此理论上与分辨率无关

        """        
        self.left_point = [
            int(self.left + self.width*0.3),
            int(self.top + self.height*0.5),
        ]
        self.right_point = [
            int(self.left + self.width*0.7),
            int(self.top + self.height*0.5),
        ]
        self.pat_point = [
            int(self.left + self.width*0.3),
            int(self.top + self.height*0.4),
        ]

    def initSummerPoint(self):
        """
        初始化夏日音游的检测点
        因为是按比例获取, 因此理论上与分辨率无关

        """        
        self.click_detect_point = [
            int(self.left + self.width*0.80),
            int(self.top + self.height*0.28),
        ]
        self.slide_detect_point = [
            int(self.left + self.width*0.80),
            int(self.top + self.height*0.22),
        ]
        self.press_detect_point = [
            int(self.left + self.width*0.85),
            int(self.top + self.height*0.26),
        ]

    def initMikuPoint(self):
        """
        初始化初音音游的检测点
        因为是按比例获取, 因此理论上与分辨率无关

        """       
        self.click_detect_point = [
            int(self.left + self.width*0.79),
            int(self.top + self.height*0.45),
        ]
        self.slide_detect_point = [
            int(self.left + self.width*0.80),
            int(self.top + self.height*0.392),
        ]
        self.press_detect_point = [
            int(self.left + self.width*0.85),
            int(self.top + self.height*0.45),
        ]

    def isSizeFit(self) -> bool:
        """判断窗口比例是否合适

        Returns:
            bool: 比例是否合适
        """        
        return round((self.width / self.height), 2) == round(16 / 9, 2)

    def press(self, point_a: list[int], point_b: list[int]=None, period: float=0) -> None:
        """模拟按住屏幕

        Args:
            point_a (list[int]): 点A
            point_b (list[int], optional): 点B
            period (float, optional): 按住时长, 默认不松开
        """        
        if point_b:
            self.press_count = 2
            tc.two_fingers_up()
            tc.two_fingers_down(point_a, point_b)
        else:
            self.press_count = 1
            tc.finger_up()
            tc.finger_down(point_a)
        if period:
            for i in range(int(period/self.frame_time)):
                self.pressing()
            self.pullUp()

    def pressing(self) -> None:
        """持续按压信号"""        
        if self.press_count == 1:
            tc.move_finger((0,0))
        elif self.press_count == 2:
            tc.move_two_fingers((0,0), (0,0))
        tc.sleep(self.frame_time)

    def pullUp(self) -> None:
        """抬起所有模拟的按下"""
        if self.press_count == 1:
            tc.finger_up()
        elif self.press_count == 2:
            tc.two_fingers_up()
        self.press_count = 0
        tc.sleep(self.frame_time)

    def click(self, point_a: list[int], point_b: list[int]=None, random_range: int=0) -> None:
        """模拟点击

        Args:
            point_a (list[int]): 点A
            point_b (list[int], optional): 点B
            random_range (int, optional): 随机点击范围
        """        
        if point_b:
            if random_range:
                random_x_a = random.randint(-random_range, random_range)
                random_y_a = random.randint(-random_range, random_range)
                random_x_b = random.randint(-random_range, random_range)
                random_y_b = random.randint(-random_range, random_range)
                tc.finger_down(
                    [point_a[0] + random_x_a, point_a[1] + random_y_a],
                    [point_b[0] + random_x_b, point_b[1] + random_y_b],
                )
            else:
                tc.two_fingers_down(point_a, point_b)
            tc.two_fingers_up()
        else:
            if random_range:
                random_x = random.randint(-random_range, random_range)
                random_y = random.randint(-random_range, random_range)
                tc.finger_down([point_a[0] + random_x, point_a[1] + random_y])
            else:
                tc.finger_down(point_a)
        tc.finger_up()

    def slideUp(self, point_a: list[int], point_b: list[int]=None, distance: int=50, period: int=3) -> None:
        """模拟上划

        Args:
            point_a (list[int]): 点A
            point_b (list[int], optional): 点B
            distance (int, optional): 上划距离, 默认50像素
            period (int, optional): 滑动持续帧数, 默认3帧
        """
        step = int(abs(distance)/period)
        if point_b:
            tc.two_fingers_down(point_a, point_b)
            for i in range(period):
                tc.move_two_fingers((0,-step), (0,-step))
                tc.sleep(self.frame_time)
            tc.two_fingers_up()
        else:
            tc.finger_down(point_a)
            for i in range(period):
                tc.move_finger((0,-step))
                tc.sleep(self.frame_time)
            tc.finger_up()

    def slideLeft(self, point_a: list[int], point_b: list[int]=None, distance: int=50, period: int=5) -> None:
        """模拟左划

        Args:
            point_a (list[int]): 点A
            point_b (list[int], optional): 点B
            distance (int, optional): 左划距离, 默认50像素
            period (int, optional): 滑动持续帧数, 默认5帧
        """
        step = int(distance/period)
        if point_b:
            tc.two_fingers_down(point_a, point_b)
            for i in range(period):
                tc.move_finger((-step, 0), (-step, 0))
                tc.sleep(self.frame_time)
        else:
            tc.finger_down(point_a)
            for i in range(period):
                tc.move_finger((-step, 0))
                tc.sleep(self.frame_time)
        self.pullUp()

    def pixelRecord(self) -> None:
        """读取像素点像素"""
        if self.window.top < 0:
            self.click_color = [0, 0, 0]
            self.slide_color = [0, 0, 0]
            self.press_color = [0, 0, 0]
            tc.sleep(self.frame_time)
            return
        try:
            with mss.mss() as sct:
                monitor = {
                    "top": self.top,
                    "left": self.left,
                    "width": self.width,
                    "height": self.height
                }
                sct_img = sct.grab(monitor)
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            self.click_color = image.getpixel((
                self.click_detect_point[0] - self.left,
                self.click_detect_point[1] - self.top,
            ))
            self.slide_color = image.getpixel((
                self.slide_detect_point[0] - self.left,
                self.slide_detect_point[1] - self.top,
            ))
            self.press_color = image.getpixel((
                self.press_detect_point[0] - self.left,
                self.press_detect_point[1] - self.top,
            ))
        except Exception as e:
            print(f"{e}")

    def colorLike(self, color: list[int], colors: list[list[int]]) -> bool:
        """判断像素点是否在颜色列表内有相似的颜色

        Args:
            color (list[int]): 指定颜色
            colors (list[list[int]]): 颜色列表

        Returns:
            bool: 是否在列表里有相似的颜色
        """        
        for c in colors:
            diff = math.sqrt((color[0] - c[0]) ** 2 + (color[1] - c[1]) ** 2 + (color[2] - c[2]) ** 2)
            if diff < self.tolerance:
                return True
        return False

    def detectAction(self) -> bool:
        """检测需要执行的动作"""
        clicker.pixelRecord()
        if self.colorLike(self.click_color, self.left_colors):
            self.action_position = "left"
            if self.past_action[-1][1] in ["press", "pressing", "needPullUp"] \
               and (self.past_action[-2][0] == self.action_position
                  or self.past_action[-2][0] == None):
                self.action_type = "pressing"
            elif self.colorLike(self.slide_color, self.left_colors):
                self.action_type = "slide"
            elif self.colorLike(self.press_color, self.left_colors):
                self.action_type = "press"
            else:
                self.action_type = "click"

        elif self.colorLike(self.click_color, self.right_colors):
            self.action_position = "right"
            if self.past_action[-1][1] in ["press", "pressing", "needPullUp"] \
               and (self.past_action[-2][0] == self.action_position
                  or self.past_action[-2][0] == None):
                self.action_type = "pressing"
            elif self.colorLike(self.slide_color, self.right_colors):
                self.action_type = "slide"
            elif self.colorLike(self.press_color, self.right_colors):
                self.action_type = "press"
            else:
                self.action_type = "click"

        elif self.colorLike(self.click_color, self.both_colors):
            self.action_position = "both"
            if self.past_action[-1][1] in ["press", "pressing", "needPullUp"] \
               and (self.past_action[-2][0] == self.action_position
                  or self.past_action[-2][0] == None):
                self.action_type = "pressing"
            elif self.colorLike(self.slide_color, self.both_colors):
                self.action_type = "slide"
            elif self.colorLike(self.press_color, self.both_colors):
                self.action_type = "press"
            else:
                self.action_type = "click"
        else:
            self.action_position = None
            if self.past_action[-1][1] == "pressing":
                self.action_type = "needPullUp"
            elif self.past_action[-1][1] == "needPullUp":
                self.action_type = "pullUp"
            else:
                self.action_type = None
            self.past_action.append([self.action_position, self.action_type])
            return True

        if self.past_action[-1][1] in ["pressing", "needPullUp"] \
            and self.past_action[-2][0] != self.action_position \
            and self.past_action[-2][0] != None:
                # 如果过快进入下一个操作，那么在此把来不及抬起的操作直接执行
                delayer.run(clicker.pullUp)
                time.sleep(self.frame_time)

        if self.past_action[-1][1] not in ["pressing", "needPullUp"] and [self.action_position, self.action_type] in self.past_action:
            # 如果不是持续按的情况下某个动作出现多次，则不执行
            return False
        elif self.action_type == "click" and (
            self.past_action[-1][1] in ["slide", "press"]
            or self.past_action[-2][1] in ["slide", "press"]
        ):
            # 如果上划或者长按马上触发的点击，则不执行
            return False
        else:
            self.past_action.append([self.action_position, self.action_type])
            return True

# 对音符进行延迟点击
class Delayer():

    def __init__(self, delay: float) -> None:
        """延迟执行器

        Args:
            delay (float): 延迟(秒)
        """        
        self.delay_time = delay

    def run(self, func: callable, *args, **kwargs) -> None:
        """多线程延迟执行指定函数

        Args:
            func (callable): 需要执行的函数
        """        
        threading.Thread(
            target=self.delay_run,
            args=(func, *args),
            kwargs=kwargs,
        ).start()

    def delay_run(self, func: callable, *args, **kwargs) -> None:
        """执行函数

        Args:
            func (callable): 需要执行的函数
        """        
        time.sleep(self.delay_time)
        func(*args, **kwargs)

if __name__ == "__main__":
    windows = pyautogui.getWindowsWithTitle("蔚蓝档案")
    if len(windows):
        clicker = Clicker(windows[0])
        # 修改此处适配不同速度，建议速度7，防止判定点连在一起
        # 夏日音游速度7
        delay = 0.62
        # 初音音游速度7
        delay = 0.58
        delayer = Delayer(delay)
        print("蔚蓝档案窗口大小:", clicker.width, clicker.height)
        print(f"当前点击延迟: {delay} 秒")
        if not clicker.isSizeFit():
            print("当前窗口大小可能不适配, 请调整为16:9的分辨率")

        clicker.initMikuPoint()

        # 测试点的位置准确性
        # clicker.press(clicker.click_detect_point)
        # tc.sleep(clicker.frame_time*10)
        # clicker.press(clicker.press_detect_point)
        # tc.sleep(clicker.frame_time*10)
        # clicker.press(clicker.slide_detect_point)

        while True:
            print(clicker.past_action[-1], round(time.time(), 2))
            # 检测缺少的颜色并添加时取消注释
            # print(clicker.click_color, clicker.slide_color)
            if not clicker.detectAction(): ...
            elif clicker.action_position != None and clicker.action_type == "pressing":
                print(f"继续按 {round(time.time(), 2)}")
                delayer.run(clicker.pressing)
            elif clicker.action_position == None and clicker.action_type == "pullUp":
                print(f"松开手 {round(time.time(), 2)}")
                delayer.run(clicker.pullUp)
            elif clicker.action_position == "left" and clicker.action_type == "click":
                print(f"左点击 {round(time.time(), 2)}")
                delayer.run(clicker.click, clicker.left_point)
            elif clicker.action_position == "left" and clicker.action_type == "slide":
                print(f"左上划 {round(time.time(), 2)}")
                delayer.run(clicker.slideUp, clicker.left_point)
            elif clicker.action_position == "left" and clicker.action_type == "press":
                print(f"左长按 {round(time.time(), 2)}")
                delayer.run(clicker.press, clicker.left_point)
            elif clicker.action_position == "right" and clicker.action_type == "click":
                print(f"右点击 {round(time.time(), 2)}")
                delayer.run(clicker.click, clicker.right_point)
            elif clicker.action_position == "right" and clicker.action_type == "slide":
                print(f"右上划 {round(time.time(), 2)}")
                delayer.run(clicker.slideUp, clicker.right_point)
            elif clicker.action_position == "right" and clicker.action_type == "press":
                print(f"右长按 {round(time.time(), 2)}")
                delayer.run(clicker.press, clicker.right_point)
            elif clicker.action_position == "both" and clicker.action_type == "click":
                print(f"左右同时点击 {round(time.time(), 2)}")
                delayer.run(clicker.click, clicker.left_point, clicker.right_point)
            elif clicker.action_position == "both" and clicker.action_type == "slide":
                print(f"左右同时上划 {round(time.time(), 2)}")
                delayer.run(clicker.slideUp, clicker.left_point, clicker.right_point)
            elif clicker.action_position == "both" and clicker.action_type == "press":
                print(f"左右同时长按 {round(time.time(), 2)}")
                delayer.run(clicker.press, clicker.left_point, clicker.right_point)
    else:
        print("未识别到正在运行的蔚蓝档案")