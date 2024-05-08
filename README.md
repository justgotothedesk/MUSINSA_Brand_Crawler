## 무신사에 입점한 브랜드 정보를 크롤링하는 프로그램 개발용 레포지토리입니다.
해당 크롤러는 무신사(MUSINSA) 사이트에서 브랜드 정보를 수집하는 데 사용됩니다. 무신사 사이트에서 특정 알파벳을 선택하고 해당 알파벳에 해당하는 브랜드를 순회하면서 브랜드 정보를 수집합니다. 이 크롤러는 Selenium을 사용하여 웹 페이지를 탐색하고, 수집한 데이터를 Excel 파일로 저장합니다. 
#
## 사용 방법
1. 해당 레포지토리를 다운 받습니다.
```bash
git clone https://github.com/justgotothedesk/MUSINSA_Brand_Crawler.git
```
2. 레포지토리 내의 requirements.txt 파일을 통해 필요한 패키지 및 라이브러리를 다운 받습니다.
```bash
pip install -r requirements.txt
```
3. 현재 사용하는 chrome과 동일한 버전의 chromedriver를 다운 받습니다.
4. 다운 받은 chromedriver의 절대 경로를 app.py 파일 내의 'CHROME_DRIVER_PATH' 변수에 입력합니다.
5. 원하는 브랜드 알파벳을 app.py 파일 내의 'brand_names' 배열에 추가합니다. (모든 알파벳을 추가해도 되지만, 크롤링 시 홈페이지 측에서 오류를 발생하게 할 수도 있기에 추천하지 않습니다.)
6. app.py 파일을 실행하여 크롤링한 데이터를 엑셀 파일로 변환합니다.
```python
python3 app.py
```
#
## 주의 사항
* 크롤러 실행 전에 Chrome 웹 드라이버가 설치되어 있어야 합니다.
* 크롤러 실행 시 Chrome 브라우저가 자동으로 열리므로, 작업 중에는 브라우저 창을 닫지 않아야 합니다.
* 크롤러 실행 시 네트워크 연결이 필요합니다.
* 크롤러 실행 시 모니터가 꺼지지 않도록 주의가 필요합니다.
