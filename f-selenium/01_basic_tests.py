from selenium import webdriver
from selenium.webdriver.common.by import By


def test_component():
    driver = setup()

    title = driver.title
    assert title == "Web form"
    # 隐式等待几秒, 等待浏览器数据加载完成
    driver.implicitly_wait(5)
    # 查找页面元素
    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    # 操作元素, 这里输入文本然后点击按钮
    text_box.send_keys("Selenium")
    submit_button.click()
    # 获取元素上的文本
    message = driver.find_element(by=By.ID, value="message")
    text = message.text
    print(f"text: {text}")
    # 结束会话, 关闭浏览器
    teardown(driver)


def setup():
    driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    return driver


def teardown(driver):
    driver.quit()
