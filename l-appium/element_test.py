from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement as MobileWebElement
import drivers
import pytest


@pytest.fixture
def driver():
    return [drivers.android_w3c_driver()]


def test_find_element_by_id(driver):
    els = driver.find_element(
        by=AppiumBy.ID,
        value="android:id/action_bar",
    )
    print("element:", els)

    assert isinstance(els, MobileWebElement)


def test_find_elements_by_id(driver):
    els = driver.find_elements(by=AppiumBy.ID, value="android:id/action_bar")
    print("elements:", els)

    assert isinstance(els[0], MobileWebElement)


def test_find_child_element(driver):
    parent = driver.find_element(by=AppiumBy.ID, value="android:id/action_bar")
    child = parent.find_elements(
        by=AppiumBy.XPATH, value="//android.widget.TextView[@text='API Demos']"
    )
    print("child element:", child)
    print("child element text:", child[0].text)

    assert isinstance(child[0], MobileWebElement)
