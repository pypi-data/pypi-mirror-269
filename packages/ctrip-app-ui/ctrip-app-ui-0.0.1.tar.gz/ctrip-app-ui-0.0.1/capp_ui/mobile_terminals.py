# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     mobile_terminals.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import shlex
import airtest
import warnings
import subprocess
import typing as t
from poco.proxy import UIObjectProxy
from airtest.cli.parser import cli_setup
from airtest.utils.transform import TargetPos

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import auto_setup, device, Template, touch, find_all, connect_device

from capp_ui.utils import logger
from capp_ui.dir import get_project_path
from capp_ui.libs import airtest_exception_format

iOS_PLATFORM = "iOS"
DEFAULT_PLATFORM = "Android"  # Android、Windows、iOS
WINDOWS_PLATFORM = "Windows"

warnings.filterwarnings("ignore", category=UserWarning,
                        message="Currently using ADB touch, the efficiency may be very low.")


def stop_app(app_name, timeout=5):
    # 构造ADB命令
    adb_cmd = "adb.exe shell am force-stop {}".format(app_name)
    # 将命令字符串分割成列表
    cmd_list = shlex.split(adb_cmd)
    try:
        # 执行ADB命令并设置超时时间
        subprocess.run(cmd_list, timeout=timeout, check=True)
        logger.info("execute cmd: {}".format(adb_cmd))
    except subprocess.TimeoutExpired:
        logger.error("Timeout occurred. Failed to stop the app.")
    except subprocess.CalledProcessError:
        logger.error("Failed to stop the app.")
    except Exception as e:
        logger.error("An error occurred: {}".format(e))


def get_screen_size_via_adb():
    # 使用ADB命令获取设备屏幕大小
    try:
        output = subprocess.check_output(['adb', 'shell', 'wm', 'size']).decode('utf-8')
        match = re.search(r'Physical size: (\d+)x(\d+)', output)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            return width, height
    except subprocess.CalledProcessError as e:
        logger.error("Error: ADB command failed: {}".format(e))
    return None


class Phone(object):

    def __init__(
            self,
            device_id: str,
            device_conn: str,
            platform: str = "Android",
            enable_debug: bool = False,
    ) -> None:
        self.platform = platform
        self.device_id = device_id
        self.device_conn = device_conn
        self.enable_debug = enable_debug
        self.__init_device()
        self.dev = device()
        self.poco = AndroidUiautomationPoco(
            use_airtest_input=True, screenshot_each_action=False
        )

    def __init_device(self) -> None:
        if not cli_setup():
            project_root = get_project_path()
            airtest.utils.compat.DEFAULT_LOG_DIR = "logs"
            airtest.core.settings.Settings.DEBUG = self.enable_debug
            airtest.core.settings.Settings.LOG_FILE = "{}.log".format(self.device_id)
            if self.device_conn.find(":5555") != -1:
                if self.platform == DEFAULT_PLATFORM:
                    connect_device(self.device_conn)
                else:
                    raise ValueError("暂时还不支持非android平台的手机初始化...")
            else:
                auto_setup(
                    project_root,
                    # logdir=True,
                    logdir=False,
                    devices=[self.device_conn],
                    project_root=project_root,
                    compress=12
                )

    @airtest_exception_format
    def shell(self, cmd: str) -> None:
        """
        在设备上执行shell命令
        platform: Android
        """
        result = None
        if self.platform == DEFAULT_PLATFORM:
            result = self.dev.shell(cmd)
            result = result.decode() if isinstance(result, bytes) else result
        return result or None

    @airtest_exception_format
    def start_app(self, app_name: str) -> None:
        """
        在设备上启动目标应用
        platform: Android, iOS
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM):
            result = self.dev.start_app(app_name)
        return result or None

    @airtest_exception_format
    def stop_app(self, app_name: str) -> None:
        """
        终止目标应用在设备上的运行
        platform: Android, iOS
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM):
            result = self.dev.stop_app(app_name)
        return result or None

    @staticmethod
    def get_cv_template(
            file_name: t.LiteralString | str | bytes,
            threshold: float = None,
            target_pos: int = TargetPos.MID,
            record_pos: tuple = None,
            resolution: tuple = (),
            rgb: bool = False,
            scale_max: int = 800,
            scale_step: float = 0.005,
    ) -> Template:
        """
        图片为触摸/滑动/等待/存在目标和图像识别需要的额外信息
        file_name str: 这是要匹配的图像文件的路径
        threshold: 表示匹配程度的阈值。阈值越低，匹配的相似度要求就越高。默认值为0.7
        target_pos: ret图片中的哪个位置，是一个二元组(10,10)
        record_pos: 指定在屏幕的哪个区域进行图像匹配。它是一个四元组 (left, top, width, height)，表示左上角坐标和宽高。
                    如果不指定，默认为整个屏幕, ((61, 2795), (61, 2962), (247, 2962), (247, 2795))
        resolution: 用于在图像匹配前对图像进行缩放。它是一个 (width, height) 的二元组，表示图像的缩放比例。默认值为 (1.0, 1.0)，即不缩放,
        rgb: 识别结果是否使用rgb三通道进行校验, 指定是否将 RGB 图像转换为灰度图像进行匹配。默认为 false，表示转换为灰度图像.
        scale_max: 多尺度模板匹配最大范围.
        scale_step: 多尺度模板匹配搜索步长.
        return: Template对象, [{'result': (517, 592), 'rectangle': ((377, 540), (377, 644), (658, 644), (658, 540)),
                'confidence': 0.9967431426048279}]
        """
        return Template(
            filename=file_name,
            threshold=threshold,
            target_pos=target_pos,
            record_pos=record_pos,
            resolution=resolution,
            rgb=rgb,
            scale_max=scale_max,
            scale_step=scale_step,
        )

    @airtest_exception_format
    def snapshot(
            self, filename: str, msg: str = "", quality: int = None, max_size: int = None
    ) -> t.Dict:
        """
        对目标设备进行一次截图，并且保存到文件中
        filename str: 保存截图的文件名，默认保存路径为 ``ST.LOG_DIR``中
        msg str:  截图文件的简短描述，将会被显示在报告页面中
        quality int:  图片的质量，[1,99]的整数，默认是10
        max_size int: 图片的最大尺寸，例如 1200
        return: {“screen”: filename, “resolution”: resolution of the screen} or None
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # Set the screenshot quality to 30
            # ST.SNAPSHOT_QUALITY = 30
            # Set the screenshot size not to exceed 600*600
            # if not set, the default size is the original image size
            # ST.IMAGE_MAXSIZE = 600
            # The quality of the screenshot is 30, and the size does not exceed 600*600
            # self.device.touch((100, 100))
            # The quality of the screenshot of this sentence is 90
            # self.device.snapshot(filename="test.png", msg="test", quality=90)
            # The quality of the screenshot is 90, and the size does not exceed 1200*1200
            # self.device.snapshot(filename="test2.png", msg="test", quality=90, max_size=1200)
            result = self.dev.snapshot(filename=filename, msg=msg, quality=quality, max_size=max_size)
        return result or None

    @airtest_exception_format
    def wake(self) -> None:
        """
        唤醒并解锁目标设备
        platform: Android
        """
        result = None
        if self.platform == DEFAULT_PLATFORM:
            result = self.dev.wake()
        return result or None

    @airtest_exception_format
    def home(self) -> None:
        """
        返回HOME界面
        platform: Android, iOS
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, iOS_PLATFORM):
            result = self.dev.home()
        return result or None

    @airtest_exception_format
    def touch(self, v: tuple | Template, times: int = 1, **kwargs) -> None:
        """
        在当前设备画面上进行一次点击
        v tuple: 点击位置，可以是一个 Template 图片实例，或是一个绝对坐标 (x, y)
        times int: 要执行的点击次数
        kwargs dict: 扩展参数，请参阅相应的文档
        return: finial position to be clicked, e.g. (100, 100)
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # temp = Template(r"tpl1606730579419.png", target_pos=5)
            # self.device.touch(temp, times=2)
            # self.device.touch((100, 100), times=2)
            # result = self.device.touch(v)
            result = touch(v=v, times=times, **kwargs)
        return result or None

    def adb_touch(self, v: tuple, timeout: int = 10) -> None:
        """
        adb 模拟操作点击，规避有些UI上无法直接点击
        """
        adb_cmd = "adb.exe -P 5037 -s {} shell input tap {} {}".format(self.device_id, v[0], v[1])
        # 将命令字符串分割成列表
        cmd_list = shlex.split(adb_cmd)
        try:
            # 执行ADB命令并设置超时时间
            subprocess.run(cmd_list, timeout=timeout, check=True)
            logger.info("execute cmd: ", adb_cmd)
        except subprocess.TimeoutExpired:
            logger.error("Timeout occurred,Failed to execute adb cmd.")
        except subprocess.CalledProcessError:
            logger.error("Failed to execute adb cmd.")
        except Exception as e:
            logger.error("An error occurred: {}".format(e))
        # touch_proxy = TouchProxy.auto_setup(self.device.adb, ori_transformer=self.device._touch_point_by_orientation)
        # touch_proxy.touch(v)

    @airtest_exception_format
    def swipe(self, v1, v2: tuple = None, duration: float = None, **kwargs) -> None:
        """
        在当前设备画面上进行一次滑动操作
        v1 tuple or Template: 滑动的起点，可以是一个Template图片实例，或是绝对坐标 (x, y)
        v2 tuple or Template: 滑动的终点，可以是一个Template图片实例，或是绝对坐标 (x, y)
        kwargs dict: 平台相关的参数 kwargs，请参考对应的平台接口文档
        return: 原点位置和目标位置
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.swipe(Template(r"tpl1606814865574.png"), vector=[-0.0316, -0.3311])
            # self.device.swipe((100, 100), (200, 200))
            # self.device.swipe((100, 100), (200, 200), duration=1, steps=6)
            # result = self.device.swipe(v1=v1, v2=v2, vector=vector, duration=duration,**kwargs)
            result = self.dev.swipe(p1=v1, p2=v2, duration=duration, **kwargs)
        return result or None

    @airtest_exception_format
    def keyevent(self, keyname: str, **kwargs) -> None:
        """
        在设备上执行keyevent按键事件
        keyname str: 平台相关的按键名称
        kwargs dict: 平台相关的参数 kwargs，请参考对应的平台接口文档
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.keyevent("HOME")
            # The constant corresponding to the home key is 3
            # self.device.keyevent("3")  # same as keyevent("HOME")
            # self.device.keyevent("BACK")
            # self.device.keyevent("KEYCODE_DEL")
            result = self.dev.keyevent(keyname=keyname, **kwargs)
        return result or None

    @airtest_exception_format
    def text(self, text: str, enter: bool = True, **kwargs) -> None:
        """
        在目标设备上输入文本，文本框需要处于激活状态
        text str: 要输入的文本
        enter bool: 是否在输入完毕后，执行一次 Enter ，默认是True
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.text("test")
            # self.device.text("test", enter=False)
            # 在Android上，有时你需要在输入完毕后点击搜索按钮
            # self.device.text("test", search=True)
            # 如果希望输入其他按键，可以用这个接口
            # self.device().yosemite_ime.code("3")  # 3 = IME_ACTION_SEARCH
            result = self.dev.text(text=text, enter=enter, **kwargs)
        return result or None

    @airtest_exception_format
    def sleep(self, secs: float = 1.0) -> None:
        """
        设置一个等待sleep时间，它将会被显示在报告中
        secs float: sleep的时长
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.sleep(1)
            result = self.dev.sleep(secs=secs)
        return result or None

    @airtest_exception_format
    def wait(
            self,
            v: Template,
            timeout: int = None,
            interval: float = 0.5,
            intervalfunc: t.Callable = None,
    ) -> t.Tuple:
        """
        等待当前画面上出现某个匹配的Template图片
        v Template: 要等待出现的目标Template实例
        timeout int: 等待匹配的最大超时时长，默认为None即默认取 ST.FIND_TIMEOUT 的值
        interval float: 尝试查找匹配项的时间间隔（以秒为单位）
        intervalfunc Callable: 在首次尝试查找匹配失败后的回调函数
        return: 匹配目标的坐标
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.wait(Template(r"tpl1606821804906.png"))  # timeout after ST.FIND_TIMEOUT
            # find Template every 3 seconds, timeout after 120 seconds
            # self.device.wait(Template(r"tpl1606821804906.png"), timeout=120, interval=3)
            # 你可以在每次查找目标失败时，指定一个回调函数
            # def notfound():
            #     print("No target found")
            # self.device.wait(Template(r"tpl1607510661400.png"), intervalfunc=notfound)
            result = self.dev.wait(v=v, timeout=timeout, interval=interval, intervalfunc=intervalfunc)
        return result or None

    @airtest_exception_format
    def exists(self, v: Template) -> t.Any:
        """ "
        检查设备上是否存在给定目标
        v Template: 要检查的目标
        return: 如果未找到目标，则返回False，否则返回目标的坐标
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # if self.device.exists(Template(r"tpl1606822430589.png")):
            #    self.device.touch(Template(r"tpl1606822430589.png"))
            # 因为 exists() 会返回坐标，我们可以直接点击坐标来减少一次图像查找
            # pos = self.device.exists(Template(r"tpl1606822430589.png"))
            # if pos:
            #    self.device.touch(pos)
            result = self.dev.exists(v=v)
        return result or None

    @airtest_exception_format
    def find_all(self, v: Template) -> t.List:
        """
        在设备屏幕上查找所有出现的目标并返回其坐标列表
        v Template: 寻找目标
        return list:  [{‘result’: (x, y), ‘rectangle’: ( (left_top, left_bottom, right_bottom, right_top) ), ‘
                        confidence’: 0.9}, …]
        platform: Android, iOS, Windows
        """
        result = list()
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.find_all(Template(r"tpl1607511235111.png"))
            result = find_all(v=v)
        return result if result else list()

    @airtest_exception_format
    def get_clipboard(self) -> str:
        """
        从剪贴板中获取内容
        return: str
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # text = self.device.get_clipboard(wda_bundle_id="com.WebDriverAgentRunner.xctrunner")
            # print(text)
            result = self.dev.get_clipboard()
        return result or None

    @airtest_exception_format
    def set_clipboard(self, content: str, *args, **kwargs) -> None:
        """
        设置剪贴板中的内容
        content str: 要设置的内容
        args tuple: 位置参数
        kwargs dict: 关键字参数
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.set_clipboard(content="content", wda_bundle_id="com.WebDriverAgentRunner.xctrunner")
            # print(self.device.get_clipboard())
            result = self.dev.set_clipboard(content=content, *args, **kwargs)
        return result or None

    @airtest_exception_format
    def paste(self, *args, **kwargs) -> None:
        """
        粘贴剪贴板中的内容
        args tuple: 位置参数
        kwargs dict: 关键字参数
        platform: Android, iOS, Windows
        """
        result = None
        if self.platform in (DEFAULT_PLATFORM, WINDOWS_PLATFORM, iOS_PLATFORM):
            # self.device.set_clipboard("content")
            # will paste "content" to the device
            # self.device.paste()
            result = self.dev.paste(*args, **kwargs)
        return result or None

    def get_po(self, type: str, name: str = '', text: str = '', desc: str = '', textMatches: str = '') -> UIObjectProxy:
        kwargs = dict()
        if type:
            kwargs["type"] = type
        if name:
            kwargs["name"] = name
        if text:
            kwargs["text"] = text
        if desc:
            kwargs["desc"] = desc
        if textMatches:
            kwargs["textMatches"] = textMatches
        return self.poco(**kwargs)

    def get_po_extend(
            self,
            type: str = "",
            name: str = "",
            text: str = "",
            desc: str = "",
            typeMatches_inner: str = "",
            nameMatches_inner: str = "",
            nameMatches_outer: str = "",
            textMatches_inner: str = "",
            textMatches_outer: str = "",
            global_num: int = None,
            local_num: int = None,
            touchable: bool = True,
    ) -> t.List:
        kwargs = dict()
        if type:
            kwargs["type"] = type
        if name:
            kwargs["name"] = name
        if text:
            kwargs["text"] = text
        if desc:
            kwargs["desc"] = desc
        if typeMatches_inner:
            kwargs["typeMatches"] = typeMatches_inner
        if nameMatches_inner:
            kwargs["nameMatches"] = nameMatches_inner
        if textMatches_inner:
            kwargs["textMatches"] = textMatches_inner
        po = self.poco(**kwargs)
        po_list = list()
        for i in po:
            po_text = i.get_text()
            po_name = i.get_name()
            if textMatches_outer and re.search(textMatches_outer, po_text) is None:
                break
            if nameMatches_outer and re.search(nameMatches_outer, po_name) is None:
                break
            zOrders = i.attr("zOrders")
            touchable_raw = i.attr("touchable")
            # pprint(get_ui_object_proxy_attr(ui_object_proxy=i))
            if zOrders.get("global") == global_num and zOrders.get("local") == local_num and touchable_raw == touchable:
                # pprint(get_ui_object_proxy_attr(ui_object_proxy=i))
                po_list.append(i)
        return po_list

    @airtest_exception_format
    def hide_keyword(self, file_name: str) -> None:
        temp = self.get_cv_template(file_name=file_name)
        hide_icon = self.find_all(v=temp)
        if len(hide_icon) > 0:
            logger.info("目前检测到键盘已打开，需要隐藏键盘，再做后续操作...")
            self.touch(v=temp)
        else:
            hw_keyword = self.poco(type="android.widget.ImageView", name="com.android.systemui:id/back", desc="返回")
            if hw_keyword.exists():
                logger.info("目前检测到HW键盘已经打开，需要隐藏键盘，再做后续操作...")
                hw_keyword.click()
            else:
                lg_keyword = self.poco(type="com.lge.ime.humaninterface.inputview.layout.HIGColoredEnterKey",
                                       name="完成")
                if lg_keyword.exists():
                    logger.info("目前检测到LG键盘已经打开，需要隐藏键盘，再做后续操作...")
                    lg_keyword.click()
                else:
                    logger.info("键盘已经隐藏，无需处理键盘...")

    # 获取元素在屏幕上的绝对坐标
    @staticmethod
    def get_abs_position(element: AndroidUiautomationPoco) -> t.Tuple:
        screen_width, screen_height = get_screen_size_via_adb()
        relative_position = element.get_position()
        absolute_x = int(relative_position[0] * screen_width)
        absolute_y = int(relative_position[1] * screen_height)
        return absolute_x, absolute_y

    # 快捷滑屏
    def quick_slide_screen(self, duration: float = 0.5):
        # 获取屏幕尺寸
        screen_width, screen_height = get_screen_size_via_adb()
        # 定义起始点和终止点坐标
        start_x = screen_width // 2  # 屏幕中心点的横坐标
        start_y = screen_height // 2  # 屏幕中心点的纵坐标
        end_x = start_x  # 横坐标保持不变
        end_y = screen_height // 4  # 终止点纵坐标为屏幕顶部 1/4 处
        # 执行滑动操作
        self.swipe((start_x, start_y), (end_x, end_y), duration=duration)
