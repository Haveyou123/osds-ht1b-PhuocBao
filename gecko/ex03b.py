from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

# Đường dẫn đến geckodriver
gecko_path = r"C:/KPDL/gecko/geckodriver.exe"
ser = Service(gecko_path)

# Tùy chọn Firefox
options = webdriver.FirefoxOptions()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False  # False để hiển thị browser

# Khởi tạo driver
driver = webdriver.Firefox(service=ser, options=options)

# Truy cập trang login
url = 'https://apps.lms.hutech.edu.vn/authn/login?next'
driver.get(url)

# Nhập thông tin người dùng
my_email = input('Please provide your email: ')
my_password = getpass.getpass('Please provide your password: ')

# Chờ và điền email/username
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'emailOrUsername'))
)
username_input.send_keys(my_email)

# Điền password
password_input = driver.find_element(By.NAME, 'password')
password_input.send_keys(my_password)

# Click nút submit
login_button = driver.find_element(By.ID, "sign-in").click()

# Chờ vài giây để đăng nhập xong
time.sleep(5)

# Kết thúc
driver.quit()
print("✅ Hoàn thành!")
