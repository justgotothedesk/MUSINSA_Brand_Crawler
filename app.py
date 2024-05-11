from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

CHROME_DRIVER_PATH = 'YOUR_PATH'
options = Options()
options.add_experimental_option("detach", True)
chrome_service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service, options=options)

# 원하는 알파벳 입력
# brand_names = ['A', 'B', 'C', 'D', 'E', 'F, 'G', 'H', 'I', 'J', 'K', 'L',
#                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'etc.']
brand_names = ['A']

# 웹페이지 열기
driver.get("https://www.musinsa.com/app/")
df = pd.DataFrame(columns=["브랜드명", "브랜드 로고", "상호", "대표자", "브랜드", "사업자번호", "통신판매업신고", "연락처", "E-mail", "영업소재지", "교환 / 반품 주소"])

yes = 0
no = 0

# 크롤링이 불가능한 브랜드명
non = {
    '브랜드명' : []
}

result = {
    '브랜드명' : [],
    '브랜드 로고' : [],
    '상호' : [],
    '대표자' : [],
    '사업자번호' : [],
    '통신판매업신고' : [],
    '연락처' : [],
    'E-mail' : [],
    '영업소재지' : [],
    '교환 / 반품 주소' : []
}

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
        
        ul_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.sc-t7vatz-11.fmkNZy"))
        )

        li_elements = WebDriverWait(ul_element, 10).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "li"))
        )

        try:
            # 브랜드 탐색
            for li_element in li_elements:
                # 브랜드명 추출
                data = {}
                en_brand_info = WebDriverWait(li_element, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.sc-55q9z5-4.fsRaYH"))
                ).text

                try:
                    # 브랜드 페이지 이동
                    a_element = WebDriverWait(li_element, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "a"))
                    )
                    href_value = a_element.get_attribute("href")
                    driver.get(href_value)
                    driver.implicitly_wait(1)
                except Exception as e:
                    print("브랜드 페이지 이상")
                    continue

                # 브랜드 로고 추출
                div_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "brand_logo.brandLogo"))
                )
                img_element = div_element.find_element(By.TAG_NAME, "img")
                img_src = img_element.get_attribute("src")

                data["브랜드명"] = en_brand_info
                data["브랜드 로고"] = img_src

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
                    print("등록된 상품이 없어, 정보가 존재하지 않습니다.")
                    non['브랜드명'].append(en_brand_info)
                    driver.execute_script("window.history.go(-1)")
                    no += 1
                    print("정상적으로 크롤링된 데이터의 갯수: ", yes)
                    print("크롤링이 불가능한 데이터의 갯수: ", no)
                    print("")
                    continue
                
                try:
                    # 판매자 정보 출력
                    time.sleep(1)
                    seller_info_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/section[3]/table"))
                    )

                    seller_info_lines = seller_info_element.text.split('\n')
                    for i in range(len(seller_info_lines)):
                        if i == 0:
                            continue
                        if i == 1:
                            key, value = seller_info_lines[i].split(' / 대표자', 1)
                            sangho, represent = value.split('/')
                            data["상호"] = sangho.strip()
                            data["대표자"] = represent.strip()
                        else:
                            key, value = seller_info_lines[i].split(' ', 1)
                            data[key.strip()] = value.strip()
                    
                    # 반송지 정보 출력
                    return_info_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/section[4]/table"))
                    )
                    
                    return_info_lines = return_info_element.text.split('\n')
                    for i in range(len(return_info_lines)):
                        if i == 0:
                            continue
                        key, value = return_info_lines[i].split('반품 주소', 1)
                        data["교환 / 반품 주소"] = value.strip()

                    for key, value in data.items():
                        print(f"{key}: {value}")
                    print('')

                except Exception as e:
                    non['브랜드명'].append(en_brand_info)
                    print("판매자 정보가 존재하지 않습니다.", e, en_brand_info)
                    no += 1 
                    print("정상적으로 크롤링된 데이터의 갯수: ", yes)
                    print("크롤링이 불가능한 데이터의 갯수: ", no)
                    print("")
                    driver.execute_script("window.history.go(-1)")               
                    driver.execute_script("window.history.go(-1)")  
                    continue

                yes += 1

                result['브랜드명'].append(data['브랜드명'])
                result['브랜드 로고'].append(data['브랜드 로고'])
                result['상호'].append(data['상호'])
                result['대표자'].append(data['대표자'])
                result['사업자번호'].append(data['사업자번호'])
                result['통신판매업신고'].append(data['통신판매업신고'])
                result['연락처'].append(data['연락처'])
                result['E-mail'].append(data['E-mail'])
                result['영업소재지'].append(data['영업소재지'])
                result['교환 / 반품 주소'].append(data['교환 / 반품 주소'])

                print("정상적으로 크롤링된 데이터의 갯수: ", yes)
                print("크롤링이 불가능한 데이터의 갯수: ", no)
                print("")

                driver.execute_script("window.history.go(-1)")               
                driver.execute_script("window.history.go(-1)")   
        except Exception as e:
            print("해당 브랜드 이상 ", e)         
            continue
            
except Exception as e:
    print("Exception occurred:", e)
    no += 1
    df = pd.DataFrame(result)
    df.set_index('브랜드명', inplace=True)
    df.to_excel(f"./{brand_names[0]}_brand_info.xlsx")

    df2 = pd.DataFrame(non)
    df2.set_index('브랜드명', inplace=True)
    df2.to_excel(f"./{brand_names[0]}_error.xlsx")

    print("일부 크롤링이 완료되었습니다.")
    print("정상적으로 크롤링된 데이터의 갯수: ", yes)
    print("크롤링이 불가능한 데이터의 갯수: ", no)

df = pd.DataFrame(result)
df.set_index('브랜드명', inplace=True)
df.to_excel(f"./{brand_names[0]}_brand_info.xlsx")

df2 = pd.DataFrame(non)
df2.set_index('브랜드명', inplace=True)
df2.to_excel(f"./{brand_names[0]}_error.xlsx")

print("일부 크롤링이 완료되었습니다.")
print("정상적으로 크롤링된 데이터의 갯수: ", yes)
print("크롤링이 불가능한 데이터의 갯수: ", no)