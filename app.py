from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_experimental_option("detach", True)
CHROME_DRIVER_PATH = '/Users/shin/Downloads/chromedriver-mac-arm64 2/chromedriver'

chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service, options=options)

brand_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'etc.']

# 웹페이지 열기
driver.get("https://www.musinsa.com/app/")

# 브랜드 클릭
try:
    brand_element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '브랜드')]"))
    )
    brand_element.click()

    # 알파벳 별로 브랜드 명 찾기
    for brand_name in brand_names:
        alphabet = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{brand_name}']"))
        )
        alphabet.click()
        time.sleep(1)
        
        ul_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.sc-t7vatz-11.fmkNZy"))
        )
        li_elements = WebDriverWait(ul_element, 10).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "li"))
        )

        # 브랜드 탐색
        for li_element in li_elements:
            # 브랜드명 추출
            en_brand_info = WebDriverWait(li_element, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sc-55q9z5-4.fsRaYH"))
            ).text
            print("브랜드명:", en_brand_info)

            # 브랜드 페이지 이동
            a_element = WebDriverWait(li_element, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "a"))
            )
            href_value = a_element.get_attribute("href")
            driver.get(href_value)
            driver.implicitly_wait(1)

            # 브랜드 로고 추출
            div_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "brand_logo.brandLogo"))
            )
            img_element = div_element.find_element(By.TAG_NAME, "img")
            img_src = img_element.get_attribute("src")
            print(f"{en_brand_info}의 이미지 소스 주소:", img_src)

            # 첫번째 상품으로 이동, 상품이 없는 경우 생략
            try:
                list_box_div = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "list-box.box"))
                )
                li_box_element = WebDriverWait(list_box_div, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, "li_box"))
                )[0]

                goods_link_element = WebDriverWait(li_box_element, 10).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "a"))
                )
                goods_href_value = goods_link_element.get_attribute("href")
                driver.get(goods_href_value)
            except Exception as e:
                print("등록된 상품이 없어, 정보가 존재하지 않습니다.\n")
                driver.execute_script("window.history.go(-1)")  
                continue

            # 판매자 정보 출력
            seller_info_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/section[3]/table"))
            )
            print(seller_info_element.text)
            
            # 반송지 정보 출력
            return_info_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/section[4]/table"))
            )
            print(return_info_element.text)
            print('\n')

            driver.execute_script("window.history.go(-1)")               
            driver.execute_script("window.history.go(-1)")               
            
except Exception as e:
    print("Exception occurred:", e)