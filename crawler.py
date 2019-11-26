import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")

# driver = webdriver.Chrome('/Users/rak/Python/chromedriver', chrome_options=options)
driver = webdriver.Chrome('/Users/rak/Python/chromedriver')
driver.implicitly_wait(3)
# 크롬 드라이버 생성 및 데이터의 완전한 로딩을 위한 3초 기다림

driver.get('http://likms.assembly.go.kr/bill/memVoteResult.do#')
# url 실행

# td_a = driver.find_element_by_css_selector('#tbody > tr:nth-child(1) > td:nth-child(1) > a')
td_a = driver.find_elements_by_css_selector('#tbody > tr > td > a')
td_a[0].click()
# congressmans = []
# for a in td_a:
#     congressmans.append(a.text)
#     # print(a.text)
# print(congressmans)



# td = driver.find_element_by_tag_name("td")

# driver.quit()
#tbody > tr:nth-child(40) > td:nth-child(7) > a
# driver.quit()
