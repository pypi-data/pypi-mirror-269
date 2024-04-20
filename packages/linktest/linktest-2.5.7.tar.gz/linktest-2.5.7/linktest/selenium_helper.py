import os
import platform
import traceback
import subprocess
from selenium import webdriver
from .webdriver_wrapper import WebDriverWrapper


try:
    import settings
except ImportError:
    traceback.print_exc()

try:
    if hasattr(settings, "run_by_github_action") and settings.run_by_github_action is True:
        pass
    else:
        # Check if the current version of chromedriver exists
        # and if it doesn't exist, download it automatically,
        # then add chromedriver to path

        try:
            from settings import auto_download_chromedriver
        except ImportError:
            auto_download_chromedriver = False

        if auto_download_chromedriver is True:
            import chromedriver_autoinstaller
            chromedriver_autoinstaller.install()
except BaseException:
    traceback.print_exc()


from . import get_project_info



class SeleniumHelper(object):
    set_implicitly_wait_flag = False

    @staticmethod
    def open_browser(ui_testcase=None, browser_name=None):
        if browser_name is None:
            if hasattr(settings, "DefaultBrowserName"):
                browser_name = settings.DefaultBrowserName
            elif hasattr(ui_testcase, "DefaultBrowserName"):
                browser_name = ui_testcase.DefaultBrowserName
            else:
                browser_name = "chrome"

        browser_name = browser_name.lower()

        if hasattr(settings, "token") and settings.token:
            # todo: 1. 如果settings.token 存在，则所有UI case 都使用此 token ?  2.  此处先实现功能为主，暂时只支持 Chrome
            if browser_name == 'chrome':
                from seleniumwire import webdriver  # Import from seleniumwire
                browser = webdriver.Chrome()

                def interceptor(request):
                    request.headers['authorization'] = "Bearer %s" % settings.token

                browser.request_interceptor = interceptor

                return browser

        elif hasattr(ui_testcase, "token"):
            if browser_name == 'chrome':
                from seleniumwire import webdriver  # Import from seleniumwire
                browser = webdriver.Chrome()

                def interceptor(request):
                    request.headers['authorization'] = "Bearer %s" % ui_testcase.token

                browser.request_interceptor = interceptor

                return browser

        else:
            from selenium import webdriver

            if browser_name == 'ie':
                browser = webdriver.Ie()
            elif browser_name == 'safari':
                browser = webdriver.Safari()
            elif browser_name == 'chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-infobars")

                if hasattr(settings, "BROWSER_OPTION"):
                    for opt in settings.BROWSER_OPTION:
                        if type(opt) is str:
                            chrome_options.add_argument(opt)
                        else:
                            raise Exception("settings.BROWSER_OPTION must be a string list!")

                if ui_testcase is None:
                    browser = webdriver.Chrome(chrome_options=chrome_options)
                else:
                    # TODO: remove below hardcode ".webrtc.", instead of providing the BROWSER_OPTION in setting/__init__.py
                    if ui_testcase.__module__.find(".webrtc.") == -1:
                        # browser = webdriver.Chrome()

                        # 使用 WebDriverWrapper 替换原来的 webdriver 实例
                        browser = WebDriverWrapper(ui_testcase)
                    else:
                        chrome_options.add_argument("--use-fake-device-for-media-stream")
                        chrome_options.add_argument("--use-fake-ui-for-media-stream")
                        chrome_options.add_argument("--incognito")

                        if platform.system() == "Darwin":
                            pass
                            # chrome_options.add_argument("--kiosk")

                        if platform.system() == "Windows":
                            chrome_options.add_argument("--start-fullscreen")

                        browser = webdriver.Chrome(chrome_options=chrome_options)

            elif browser_name in ('firefox', 'ff'):
                profile = webdriver.FirefoxProfile(settings.FIREFOX_PROFILE)
                profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")
                if ui_testcase.__module__.find("tests.webrtc.") == -1:
                    browser = webdriver.Firefox()
                else:
                    profile.set_preference("media.navigator.permission.disabled", "true")
                    profile.set_preference("browser.dom.window.dump.enabled", "true")
                    browser = webdriver.Firefox(firefox_profile=profile)
            elif browser_name == 'device':
                from appium import webdriver as mobiledriver
                browser = mobiledriver.Remote(
                    command_executor='http://' + ui_testcase.appium_server_ip + ':' + ui_testcase.appium_server_port
                                     + '/wd/hub', desired_capabilities=ui_testcase.capability)

        try:
            browser.maximize_window()
        except BaseException:
            traceback.print_exc()

        if SeleniumHelper.set_implicitly_wait_flag is False:
            # user can set the "WEBDRIVER_IMPLICIT_WAIT" in settings.
            # eg: WEBDRIVER_IMPLICIT_WAIT = 60
            # if there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20 (in seconds)
            if hasattr(settings, "WEBDRIVER_IMPLICIT_WAIT"):
                if type(settings.WEBDRIVER_IMPLICIT_WAIT) == int or type(settings.WEBDRIVER_IMPLICIT_WAIT) == float:
                    browser.implicitly_wait(settings.WEBDRIVER_IMPLICIT_WAIT)
                    print("set WEBDRIVER_IMPLICIT_WAIT: %s" % settings.WEBDRIVER_IMPLICIT_WAIT)
                else:
                    # if the type of settings.WEBDRIVER_IMPLICIT_WAIT is not correct, here set a default value: 20
                    browser.implicitly_wait(20)
                    print(
                        "the type of WEBDRIVER_IMPLICIT_WAIT:%s is not 'int' or 'float', here set a default value: 20")
            else:
                # if there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20
                browser.implicitly_wait(20)
                print(
                    "there are no WEBDRIVER_IMPLICIT_WAIT found in settings, then set a default value: 20")

            # set SeleniumHelper.set_implicitly_wait_flag = True after set the WEBDRIVER_IMPLICIT_WAIT.
            SeleniumHelper.set_implicitly_wait_flag = True

        return browser

    @staticmethod
    def switch_to_new_window(browser, old_handle_list=None):
        """
        this is used to switch to new window.
        Note: if there are only two windows, the old_handle_list can be the default value: None, the new window will be selected.
              if there are more than two windows, the old_handle_list should be the list of older window's handle, the new window will be selected
        """
        old_handle = browser.current_window_handle
        handles = browser.window_handles

        for handle in handles:
            if old_handle_list == None:
                if handle == old_handle:
                    print("%s is the old window's handler" % (handle))
                else:
                    print("%s is the new window's handler" % (handle))
                    break
            else:
                if handle in old_handle_list:
                    print("%s is the old window's handler" % (handle))
                else:
                    print("%s is the new window's handler" % (handle))
                    break

        browser.switch_to_window(handle)
