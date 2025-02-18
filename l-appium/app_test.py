import drivers
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.applicationstate import ApplicationState
import pytest

_package_name_ = "io.appium.android.apis"


# @pytest.fixture
# def driver():
#     return drivers.android_w3c_driver()


def test_install_app(driver):
    result = driver.install_app("ApiDemos-debug.apk")
    print("install_app:", result)
    assert isinstance(result, WebDriver)


def test_remove_app(driver):
    result = driver.remove_app(_package_name_)
    print("remove_app:", result)
    assert isinstance(result, WebDriver)


def test_is_app_installed(driver):
    result = driver.is_app_installed(_package_name_)
    print("is_app_installed:", result)
    assert isinstance(result, bool)


def test_terminate_app(driver):
    result = driver.terminate_app(_package_name_)
    print("terminate_app:", result)
    assert isinstance(result, bool)


def test_activate_app(driver):
    result = driver.activate_app(_package_name_)
    print("activate_app:", result)
    assert isinstance(result, WebDriver)


def test_backgroup_app(driver):
    result = driver.backgroup_app(0)
    print("backgroup_app:", result)
    assert isinstance(result, WebDriver)


def test_query_app_state(driver):
    result = driver.query_app_state(_package_name_)
    print("query_app_state:", result)
    assert result is ApplicationState.RUNNING_IN_FOREGROUND


def test_app_strings(driver):
    result = driver.app_strings()
    print("app_strings:", result)
