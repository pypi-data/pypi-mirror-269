"""
WebDriverWrapper 类说明文档
作者：Lin Wang

概述：
WebDriverWrapper 类是一个对 Selenium WebDriver (特别是 Chrome 类) 的扩展，用于在执行 Web UI 测试时自动记录 webdriver 操作。
当调用常用的方法，如 get、find_element、click 等时，这些操作将自动记录到 logger 中。

使用说明：
1. 导入 WebDriverWrapper 类：
   从 webdriver_wrapper 模块导入 WebDriverWrapper 类。

2. 创建 WebDriverWrapper 实例：
   在测试框架中，使用 WebDriverWrapper 类替换原来的 Chrome webdriver 实例。将 logger 对象和其他所需参数传入 WebDriverWrapper 的构造函数中。

示例代码：

from selenium.webdriver import ChromeOptions
from webdriver_wrapper import WebDriverWrapper

class MyTestCase:
    def __init__(self, logger):
        self.logger = logger
        chrome_options = ChromeOptions()
        # 使用 WebDriverWrapper 替换原来的 webdriver 实例
        self.browser = WebDriverWrapper(self.logger, options=chrome_options)

    def run_test(self):
        self.browser.get("https://www.bing.com")
        # 其他测试代码

功能说明：
1. _log_action 方法：
   用于记录操作到 logger。在为其他 webdriver 方法添加日志记录功能时，可以调用此方法。

2. 常用方法的日志记录功能：
   WebDriverWrapper 类已经为以下方法添加了日志记录功能：
   - get
   - find_element
   - find_elements
   - execute_script

   根据需要，您可以继续为其他 webdriver 方法添加日志记录功能，只需在 WebDriverWrapper 类中重写这些方法并调用 _log_action() 即可。
"""
import os
import typing
from typing import List
from typing import Dict
from typing import Optional
from typing import Union

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.remote.webelement import WebElement

AUTO_SCREENSHOT_ON_ACTION = False

try:
    import settings
except BaseException:
    raise ("No settings module found ....")

try:
    from settings import AUTO_SCREENSHOT_ON_ACTION

    AUTO_SCREENSHOT_ON_ACTION = settings.AUTO_SCREENSHOT_ON_ACTION
except ImportError:
    settings.AUTO_SCREENSHOT_ON_ACTION = False


class WebElementWrapper:
    def __init__(self, element, logger, this):
        self.element = element
        self.logger = logger
        self.webdriver_wrapper = this

    def _log_action(self, action, *args):
        if args:
            msg = f"- WebElement Action: '{action}' with args: {', '.join(map(str, args))}"
        else:
            msg = f"- WebElement Action: '{action}'"
        self.logger.info(msg)

        if AUTO_SCREENSHOT_ON_ACTION:
            self.webdriver_wrapper.save_screenshot()

    def send_keys(self, *value):
        self.element.send_keys(*value)

        if value and value[0] == Keys.ENTER:
            self._log_action("send_keys", "Keys.ENTER")
        elif value and value[0] == Keys.CANCEL:
            self._log_action("send_keys", "Keys.CANCEL")
        elif value and value[0] == Keys.ESCAPE:
            self._log_action("send_keys", "Keys.ESCAPE")
        elif value and value[0] == Keys.SPACE:
            self._log_action("send_keys", "Keys.SPACE")
        elif value and value[0] == Keys.TAB:
            self._log_action("send_keys", "Keys.TAB")
        elif value and value[0] == Keys.BACKSPACE:
            self._log_action("send_keys", "Keys.BACKSPACE")
        elif value and value[0] == Keys.DELETE:
            self._log_action("send_keys", "Keys.DELETE")
        else:
            self._log_action("send_keys", *value)

    def click(self):
        self.element.click()
        self._log_action("click")

    def clear(self):
        self.element.clear()
        self._log_action("clear")

    def tag_name(self) -> str:
        return_value = self.element.tag_name
        self._log_action("tag_name")
        return return_value

    def submit(self):
        self.element.submit()
        self._log_action("submit")

    def text(self) -> str:
        return_value = self.element.text
        self._log_action("text")
        return return_value

    def get_property(self, name) -> Union[str, bool, WebElement, dict]:
        return_value = self.element.get_property(name)
        self._log_action("get_property", name)
        return return_value

    def get_dom_attribute(self, name) -> str:
        return_value = self.element.get_dom_attribute(name)
        self._log_action("get_dom_attribute", name)
        return return_value

    def get_attribute(self, name) -> Union[str, None]:
        return_value = self.element.get_attribute(name)
        self._log_action("get_attribute", name)
        return return_value

    def is_selected(self) -> bool:
        return_value = self.element.is_selected()
        self._log_action("is_selected")
        return return_value

    def is_enabled(self) -> bool:
        return_value = self.element.is_enabled()
        self._log_action("is_enabled")
        return return_value

    def is_displayed(self) -> bool:
        return_value = self.element.is_displayed()
        self._log_action("is_displayed")
        return return_value

    def location_once_scrolled_into_view(self) -> dict:
        return_value = self.element.location_once_scrolled_into_view
        self._log_action("location_once_scrolled_into_view")
        return return_value

    def size(self) -> dict:
        return_value = self.element.size
        self._log_action("size")
        return return_value

    def value_of_css_property(self, property_name) -> str:
        return_value = self.element.value_of_css_property(property_name)
        self._log_action("value_of_css_property", property_name)
        return return_value

    def location(self) -> dict:
        return_value = self.element.location
        self._log_action("location")
        return return_value

    def rect(self) -> dict:
        return_value = self.element.rect
        self._log_action("rect")
        return return_value

    def screenshot_as_base64(self) -> str:
        return_value = self.element.screenshot_as_base64
        self._log_action("screenshot_as_base64")
        return return_value

    def screenshot_as_png(self) -> bytes:
        return_value = self.element.screenshot_as_png
        self._log_action("screenshot_as_png")
        return return_value

    def screenshot(self, filename) -> bool:
        return_value = self.element.screenshot(filename)
        self._log_action("screenshot", filename)
        return return_value

    def parent(self):
        return_value = self.element.parent
        self._log_action("parent")
        return return_value

    def id(self) -> str:
        return_value = self.element.id
        self._log_action("id")
        return return_value

    def find_element(self, by=By.ID, value=None) -> WebElement:
        return_value = self.element.find_element(by, value)
        self._log_action("find_element", by, value)
        return return_value

    def find_elements(self, by=By.ID, value=None) -> List[WebElement]:
        return_value = self.element.find_elements(by, value)
        self._log_action("find_elements", by, value)
        return return_value

    def __hash__(self) -> int:
        return_value = self.element.__hash__()
        self._log_action("__hash__")
        return return_value

    # todo:可以继续封装 WebElement 的其他方法


class WebDriverWrapper(Chrome):
    def __init__(self, ui_testcase, *args, **kwargs):
        self.logger = ui_testcase.logger
        self.ui_testcase = ui_testcase

        # Default options and service for Chrome, if not provided in kwargs
        options = kwargs.pop('options', Options())
        service = None # todo macOS VS windows
        keep_alive = kwargs.pop('keep_alive', True)

        # Initialization of the Chrome WebDriver with the correct parameters
        super().__init__(options=options, service=service, keep_alive=keep_alive, *args, **kwargs)

    def _log_action(self, action, *args):
        if args:
            msg = f"- WebDriver Action: '{action}' with args: {', '.join(map(str, args))}"
        else:
            msg = f"- WebDriver Action: '{action}'"
        self.logger.info(msg)


    def get(self, url):
        super().get(url)
        self._log_action("get", url)
        if AUTO_SCREENSHOT_ON_ACTION:
            self.save_screenshot()

    # def find_element(self, by=By.ID, value=None):
    #     self._log_action("find_element", by, value)
    #     element = super().find_element(by, value)
    #     this = self
    #     return WebElementWrapper(element, self.logger, this)

    def find_element(self, by=By.ID, value=None):
        element = super().find_element(by, value)
        this = self
        return_value = WebElementWrapper(element, self.logger, this)
        self._log_action("find_element", by, value)
        return return_value

    def find_elements(self, by=By.ID, value=None):
        return_value = super().find_elements(by, value)
        self._log_action("find_elements", by, value)
        return return_value

    def execute_script(self, script, *args):
        return_value = super().execute_script(script, *args)
        self._log_action("execute_script", script, *args)
        return return_value

    # def execute(self, driver_command: str, params: dict = None) -> dict:
    #     self._log_action("execute", driver_command, params)
    #     return super().execute(driver_command, params)

    def execute_async_script(self, script: str, *args):
        return_value = super().execute_async_script(script, *args)
        self._log_action("execute_async_script", script, *args)
        return return_value

    def title(self) -> str:
        return_value = super().title
        self._log_action("title")
        return return_value

    # def create_web_element(self, element_id: str) -> WebElement:
    #     self._log_action("create_web_element", element_id)
    #     return super().create_web_element(element_id)

    def start_session(self, capabilities: dict) -> None:
        super().start_session(capabilities)
        self._log_action("start_session", capabilities)

    def current_url(self) -> str:
        return_value = super().current_url
        self._log_action("current_url")
        return return_value

    def page_source(self) -> str:
        return_value = super().page_source
        self._log_action("page_source")
        return return_value

    def close(self) -> None:
        super().close()
        self._log_action("close")

    def quit(self) -> None:
        super().quit()
        self._log_action("quit")

    def current_window_handle(self) -> str:
        return_value = super().current_window_handle
        self._log_action("current_window_handle")
        return return_value

    def window_handles(self) -> List[str]:
        return_value = super().window_handles
        self._log_action("window_handles")
        return return_value

    def maximize_window(self) -> None:
        super().maximize_window()
        self._log_action("maximize_window")

    def fullscreen_window(self) -> None:
        super().fullscreen_window()
        self._log_action("fullscreen_window")

    def minimize_window(self) -> None:
        super().minimize_window()
        self._log_action("minimize_window")

    def get_cookie(self, name) -> typing.Optional[typing.Dict]:
        return_value = super().get_cookie(name)
        self._log_action("get_cookie", name)
        return return_value

    def refresh(self) -> None:
        super().refresh()
        self._log_action("refresh")
        if AUTO_SCREENSHOT_ON_ACTION:
            self.save_screenshot()

    def forward(self) -> None:
        super().forward()
        self._log_action("forward")
        if AUTO_SCREENSHOT_ON_ACTION:
            self.save_screenshot()

    def back(self) -> None:
        super().back()
        self._log_action("back")
        if AUTO_SCREENSHOT_ON_ACTION:
            self.save_screenshot()

    def get_cookies(self) -> List[dict]:
        return_value = super().get_cookies()
        self._log_action("get_cookies")
        return return_value

    def add_cookie(self, cookie_dict) -> None:
        super().add_cookie(cookie_dict)
        self._log_action("add_cookie", cookie_dict)

    def delete_cookie(self, name) -> None:
        super().delete_cookie(name)
        self._log_action("delete_cookie", name)

    def delete_all_cookies(self) -> None:
        super().delete_all_cookies()
        self._log_action("delete_all_cookies")

    def implicitly_wait(self, time_to_wait: float) -> None:
        super().implicitly_wait(time_to_wait)
        self._log_action("implicitly_wait", time_to_wait)

    def set_script_timeout(self, time_to_wait: float) -> None:
        super().set_script_timeout(time_to_wait)
        self._log_action("set_script_timeout", time_to_wait)

    def set_page_load_timeout(self, time_to_wait: float) -> None:
        super().set_page_load_timeout(time_to_wait)
        self._log_action("set_page_load_timeout", time_to_wait)

    def save_screenshot(self, filename=None) -> bool:
        # todo: filename 不为 None 时
        if filename is None:
            if not getattr(self.ui_testcase, 'linktest_screenshot_index', False):
                setattr(self.ui_testcase, 'linktest_screenshot_index', 1)
            else:
                self.ui_testcase.linktest_screenshot_index += 1

            if self.ui_testcase.rerun_tag == 1:
                filename = self.ui_testcase.full_tc_folder + os.sep + self.logger.name + "_rerun_" + str(self.ui_testcase.linktest_screenshot_index) + "_screenshot.png"
            else:
                filename = self.ui_testcase.full_tc_folder + os.sep + self.logger.name + "_" + str(self.ui_testcase.linktest_screenshot_index) + "_screenshot.png"

        self._log_action("save_screenshot", filename)

        return super().save_screenshot(filename)

    # todo 可以继续在此处添加其他 WebDriver 方法的日志记录功能
