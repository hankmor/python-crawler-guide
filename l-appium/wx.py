import os
from sys import exc_info
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android.uiautomator2.base import UiAutomator2Options

# from pymongo import MongoClient
import re
import time

# 平台
PLATFORM = "Android"

# 设备名称 通过 adb devices -l 获取
DEVICE_NAME = "M2007J17C"

# APP路径
APP = os.path.abspath(".") + "/weixin.apk"

# APP包名
APP_PACKAGE = "com.tencent.mm"

# 入口类名
APP_ACTIVITY = ".ui.LauncherUI"

# Appium地址
DRIVER_SERVER = "http://127.0.0.1:4723"
# 等待元素加载时间
TIMEOUT = 300

# 微信手机号密码
USERNAME = ""
PASSWORD = ""

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 700

# MongoDB配置
MONGO_URL = "localhost"
MONGO_DB = "moments"
MONGO_COLLECTION = "moments"

# 滑动间隔
SCROLL_SLEEP_TIME = 1


class Moments:
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": "M2007J17C",
            "appium:udid": "50952d27",
            "appium:appPackage": "com.tencent.mm",
            "appium:appActivity": ".ui.LauncherUI",
            "appium:noReset": True,  # no need to reset app, make no need to login
        }
        options = UiAutomator2Options()
        options.load_capabilities(self.desired_caps)
        self.driver = webdriver.Remote(DRIVER_SERVER, options=options)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        # self.client = MongoClient(MONGO_URL)
        # self.db = self.client[MONGO_DB]
        # self.collection = self.db[MONGO_COLLECTION]
        # 处理器
        self.processor = Processor()

    def login(self):
        """
        登录微信
        :return:
        """
        # 登录按钮
        login = self.wait.until(
            EC.presence_of_element_located((By.ID, "com.tencent.mm:id/cjk"))
        )
        login.click()
        # 手机输入
        phone = self.wait.until(
            EC.presence_of_element_located((By.ID, "com.tencent.mm:id/h2"))
        )
        phone.set_text(USERNAME)
        # 下一步
        next = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/adj"))
        )
        next.click()
        # 密码
        password = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@resource-id="com.tencent.mm:id/h2"][1]')
            )
        )
        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/adj"))
        )
        submit.click()

    def enter(self):
        """
        进入朋友圈
        :return:
        """
        # 选项卡
        tab = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@resource-id="com.tencent.mm:id/bw3"][3]')
            )
        )
        tab.click()
        # 朋友圈
        moments = self.wait.until(
            EC.presence_of_element_located((By.ID, "com.tencent.mm:id/atz"))
        )
        moments.click()

    def crawl(self):
        """
        爬取
        :return:
        """
        while True:
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        '//androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.RelativeLayout',
                    )
                )
            )
            avatar, nickname, content, date = "", "", "", ""
            # 遍历每条状态
            for item in items:
                print("----------")

                try:
                    # 头像
                    avatar = item.find_element(
                        By.XPATH, '(//android.widget.ImageView[@content-desc="头像"])'
                    ).get_attribute("content-desc")
                except NoSuchElementException:
                    print("no avatar")
                try:
                    # 昵称
                    el = item.find_element(
                        By.XPATH,
                        "//android.widget.LinearLayout/android.view.ViewGroup/*[1]",
                    )
                    nickname = el.get_attribute("text")
                except NoSuchElementException:
                    print("no nickname")
                try:
                    # 正文
                    el = item.find_element(
                        By.XPATH,
                        "//android.widget.LinearLayout/android.view.ViewGroup/*[2]",
                    )
                    print("tag name:", el.tag_name)
                    # if el.tag_name == "android.widget.RelativeLayout":
                    #     content = "android.widget.RelativeLayout"
                        # content += self.try_read_content(el)
                    # elif el.tag_name == "android.widget.LinearLayout":
                    #     content = "android.widget.LinearLayout"
                    try:
                        el = el.find_element(
                            By.XPATH, "/android.widget.FrameLayout"
                        )
                        content = "compose content"
                        content += self.try_read_content(el)
                    except NoSuchElementException:
                        content += self.try_read_content(el)
                    # else:
                    #     content = "unknown content"
                except NoSuchElementException:
                    print("invalid content")
                try:
                    # 日期
                    date = item.find_element(
                        By.XPATH,
                        "//android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout//android.widget.TextView",
                    ).get_attribute("text")
                    # 处理日期
                    date = self.processor.date(date)
                    print(nickname, content, date)
                except NoSuchElementException:
                    print("parse date error")
                print("avatar: %s" % avatar)
                print("nickname: %s" % nickname)
                print("content: %s" % content)
                print("date: %s" % date)


                time.sleep(SCROLL_SLEEP_TIME)

            # 上滑
            self.driver.swipe(
                FLICK_START_X,
                FLICK_START_Y + FLICK_DISTANCE,
                FLICK_START_X,
                FLICK_START_Y,
            )

    def try_read_content(self, el):
        content = ""
        try:
            el = el.find_element(By.XPATH, "//*[@content-desc='视频']")
            content += "\nthis is a video"
        except NoSuchElementException:
            pass
        try:
            el = el.find_element(By.XPATH, "//android.widget.ImageView")
            content += "\ncontent contains images"
        except NoSuchElementException:
            pass
        try:
            el = el.find_element(By.XPATH, "//android.widget.TextView")
            content = "\ncontent contains text:" + el.text
        except NoSuchElementException:
            pass
        return content

    def main(self):
        """
        入口
        :return:
        """
        # 登录
        self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()


class Processor:
    def date(self, datetime):
        """
        处理时间
        :param datetime: 原始时间
        :return: 处理后时间
        """
        if re.match("\d+分钟前", datetime):
            minute = re.match("(\d+)", datetime).group(1)
            datetime = time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - float(minute) * 60)
            )
        if re.match("\d+小时前", datetime):
            hour = re.match("(\d+)", datetime).group(1)
            datetime = time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - float(hour) * 60 * 60)
            )
        if re.match("昨天", datetime):
            datetime = time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - 24 * 60 * 60)
            )
        if re.match("\d+天前", datetime):
            day = re.match("(\d+)", datetime).group(1)
            datetime = time.strftime(
                "%Y-%m-%d", time.localtime(time.time() - float(day) * 24 * 60 * 60)
            )
        return datetime


if __name__ == "__main__":
    moments = Moments()
    # moments.main()
    moments.crawl()
