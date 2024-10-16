import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def send_mail(subject, body):
    """
    使用 mail 命令发送邮件通知
    """
    process = subprocess.Popen(['mail', '-s', subject, 'syh@localhost'], stdin=subprocess.PIPE)
    process.communicate(input=body.encode())

# 配置 Firefox 无头模式
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # 无头模式
service = Service("/usr/bin/geckodriver")  # 确保 geckodriver 在正确路径

# 启动 Firefox 浏览器
driver = webdriver.Firefox(service=service, options=options)

try:
    # 访问页面
    # print("打开页面")
    driver.get("https://paofu.cloud")

    # 等待并点击“登入”按钮
    # print("等待登录按钮")
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "登入"))
    )
    # print("找到并点击登录按钮")
    login_button.click()

    # 等待用户名输入框加载并输入电子邮件
    # print("等待用户名输入框")
    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "email")
        )  # 使用 By.ID 来选择 email 输入框
    )
    # print("输入用户名")
    username_field.send_keys("your_email@example.com")  # 替换为你的电子邮件

    # 等待密码输入框加载并输入密码
    # print("等待密码输入框")
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "password")
        )  # 使用 By.ID 来选择 password 输入框
    )
    # print("输入密码")
    password_field.send_keys("your_password")  # 替换为你的密码

    # print("提交登录表单")

    # 1. 可以按 Enter 键提交登录表单
    password_field.send_keys(Keys.RETURN)  # 模拟按下回车键

    # 检查是否已经签到
    # print("检查是否已经签到")
    # 使用 XPath 选择可能的签到按钮或“明日再来”按钮
    try:
        checkin_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//a[contains(@class, "btn-primary") and contains(text(), "每日签到")]',
                )
            )
        )
        # print("找到签到按钮，点击签到")
        checkin_button.click()
        send_mail("签到成功！", "签到成功！")

    except:
        # 如果没有找到签到按钮，检查是否存在“明日再来”按钮
        already_checked_in = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//a[contains(@class, "btn-primary") and contains(text(), "明日再来")]',
                )
            )
        )
        send_mail("已签到，今日无需再签到。", "已签到，今日无需再签到。")


except Exception as e:
    print(f"出现错误: {e}")

finally:
    driver.quit()
