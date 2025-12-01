from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

gecko_path = r"C:/KPDL/gecko/geckodriver.exe"
service = Service(gecko_path)

# Cấu hình Firefox options
options = webdriver.FirefoxOptions()  # Sửa: firefox.options.Options() -> FirefoxOptions()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
# options.headless = False  # Không cần dòng này, mặc định là False

# Khởi tạo driver (chỉ cần 1 lần, bạn đang khởi tạo 2 lần)
driver = webdriver.Firefox(service=service, options=options)

# Tạo url
url = 'https://gochek.vn/collections/all'

# Truy cập
driver.get(url)
print("✅ Đã truy cập:", url)
time.sleep(5)

# Danh sách lưu dữ liệu
products_data = []

# Hàm cuộn trang để load thêm sản phẩm
def scroll_page(times=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(times):
        # Cuộn xuống cuối trang
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Tính chiều cao mới
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"🔄 Đã cuộn lần {i+1} - Chiều cao: {new_height}px")
        
        # Nếu không còn nội dung mới thì dừng
        if new_height == last_height:
            print("✅ Đã load hết sản phẩm")
            break
        last_height = new_height

# Cuộn để load hết sản phẩm
scroll_page(15)

# Tìm tất cả sản phẩm
try:
    products = driver.find_elements(By.CSS_SELECTOR, ".product-block.product-resize")
    print(f"\n✅ Tìm thấy {len(products)} sản phẩm\n")
    
    for idx, product in enumerate(products, 1):
        try:
            # Tên sản phẩm
            try:
                name = product.find_element(By.CSS_SELECTOR, ".pro-name a").text.strip()
            except:
                name = "N/A"
            
            # Link sản phẩm
            try:
                link = product.find_element(By.CSS_SELECTOR, ".pro-name a").get_attribute("href")
            except:
                link = "N/A"
            
            # Giá khuyến mãi (giá hiện tại)
            try:
                sale_price = product.find_element(By.CSS_SELECTOR, ".box-pro-prices .pro-price.highlight span").text.strip()
            except:
                try:
                    sale_price = product.find_element(By.CSS_SELECTOR, ".pro-price-mb .pro-price").text.strip()
                except:
                    sale_price = "N/A"
            
            # Giá gốc
            try:
                original_price = product.find_element(By.CSS_SELECTOR, ".pro-price-del .compare-price").text.strip()
            except:
                original_price = sale_price  # Nếu không có giá gốc thì lấy giá sale
            
            # Phần trăm giảm giá
            try:
                discount = product.find_element(By.CSS_SELECTOR, ".product-sale span").text.strip()
            except:
                discount = "N/A"
            
            # Bảo hành - thường không có trên trang listing, cần vào chi tiết sản phẩm
            warranty = "N/A"
            
            # Lưu dữ liệu
            product_info = {
                "STT": idx,
                "Tên sản phẩm": name,
                "Giá gốc": original_price,
                "Giá khuyến mãi": sale_price,
                "Giảm giá": discount,
                "Bảo hành": warranty,
                "Link": link
            }
            
            products_data.append(product_info)
            print(f"✅ [{idx}] {name}")
            print(f"   💰 Giá: {original_price} → {sale_price} ({discount})")
            print(f"   🔗 {link}\n")
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy thông tin sản phẩm {idx}: {e}\n")
            continue
    
except Exception as e:
    print(f"❌ Lỗi khi tìm sản phẩm: {e}")

# Đóng browser
driver.quit()
print("\n" + "="*60)

# Lưu vào Excel
if products_data:
    df = pd.DataFrame(products_data)
    output_file = "gochek_products.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"✅ Đã lưu {len(products_data)} sản phẩm vào file: {output_file}")
    print("="*60)
    print("\n📊 PREVIEW DỮ LIỆU (5 sản phẩm đầu):\n")
    print(df.head().to_string(index=False))
else:
    print("Không có dữ liệu để lưu")

print("HOÀN THÀNH!")