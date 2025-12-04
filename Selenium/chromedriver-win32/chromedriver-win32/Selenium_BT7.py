from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
# URL thể loại Wikipedia
start_url = "https://vi.wikipedia.org/wiki/Th%E1%BB%83_lo%E1%BA%A1i:Tr%C6%B0%E1%BB%9Dng_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"

driver = webdriver.Chrome()

all_links = []      # Danh sách link trường
records = []        # Dữ liệu thu được

# -------------------------
# B1: Lấy link các trường
# -------------------------
driver.get(start_url)
time.sleep(2)

items = driver.find_elements(By.CSS_SELECTOR, "#mw-pages .mw-category-group li a")

for a in items:
    link = a.get_attribute("href")

    # Chỉ lấy bài viết thật
    if link and link.startswith("https://vi.wikipedia.org/wiki/"):
        title = link.split("/wiki/")[1]
        if ":" not in title:           # bỏ Thể_loại:, File:, Thành_viên:
            all_links.append(link)

print("Số trường lấy được:", len(all_links))

# -------------------------
# B2: Lấy thông tin từng trường
# -------------------------
for i, link in enumerate(all_links, start=1):
    print(f"[{i}] Đang lấy:", link)
    driver.get(link)
    time.sleep(1)

    # Tên trường
    try:
        name = driver.find_element(By.ID, "firstHeading").text
    except:
        name = ""

    ma = ""
    hieu_truong = ""
    website = ""

    # Duyệt các dòng trong bảng infobox
    rows = driver.find_elements(By.CSS_SELECTOR, "table.infobox tr")
    for row in rows:
        try:
            th = row.find_element(By.TAG_NAME, "th").text
            td = row.find_element(By.TAG_NAME, "td").text
        except:
            continue

        if "Mã trường" in th:
            ma = td
        if "Hiệu trưởng" in th:
            hieu_truong = td
        if "Website" in th or "Trang web" in th:
            try:
                website = row.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                website = td

    records.append({
        "Tên trường": name,
        "Mã trường": ma,
        "Hiệu trưởng": hieu_truong,
        "Website": website,
        "Link wiki": link
    })

# -------------------------
# B3: Xuất CSV
# -------------------------
df = pd.DataFrame(records)
df.to_csv("truong_caodang.csv", index=False, encoding="utf-8-sig")

driver.quit()
print(df.head())
