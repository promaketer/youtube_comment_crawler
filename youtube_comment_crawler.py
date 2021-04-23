from selenium import webdriver
import time
from openpyxl import Workbook
import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

wb = Workbook(write_only=True)
ws = wb.create_sheet()

driver = webdriver.Chrome()

# URL에 댓글 추출 필요한 유튜브 영상 주소 기입
driver.get("URL")
driver.implicitly_wait(3)

driver.execute_script("window.scrollTo(0, 800)")
time.sleep(1)

# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(0.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)

# 팝업 닫기
try:
    driver.find_element_by_css_selector("#dismiss-button > a").click()
except:
    pass

# 대댓글 모두 열기
buttons = driver.find_elements_by_css_selector("#more-replies > a")

time.sleep(1)

for button in buttons:
    button.send_keys(Keys.ENTER)
    button.click()

time.sleep(1)

# 정보 추출하기
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select("div#header-author > h3 > #author-text > span")
comment_list = soup.select("yt-formatted-string#content-text")

id_final = []
comment_final = []

for i in range(len(comment_list)):
    temp_id = id_list[i].text
    temp_id = temp_id.replace('\n', '')
    temp_id = temp_id.replace('\t', '')
    temp_id = temp_id.replace('    ', '')
    id_final.append(temp_id)

    temp_comment = comment_list[i].text
    temp_comment = temp_comment.replace('\n', '')
    temp_comment = temp_comment.replace('\t', '')
    temp_comment = temp_comment.replace('    ', '')
    comment_final.append(temp_comment)

pd_data = {"아이디" : id_final , "댓글 내용" : comment_final}
youtube_pd = pd.DataFrame(pd_data)

# 파일명에 원하는 이름의 파일명 기입
youtube_pd.to_excel('파일명.xlsx')