import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")

# driver = webdriver.Chrome('/Users/rak/Python/chromedriver', chrome_options=options)
# >>> headless로 드라이버 실행

driver = webdriver.Chrome('/Users/rak/Python/chromedriver')
driver.implicitly_wait(3)
# >>> 크롬 드라이버 생성 및 데이터의 완전한 로딩을 위한 3초 기다림

driver.get('http://likms.assembly.go.kr/bill/memVoteResult.do#')
# >>> url 실행

congressmans = []
congressmanName = ''
# td_a = driver.find_element_by_css_selector('#tbody > tr:nth-child(1) > td:nth-child(1) > a')
td_a = driver.find_elements_by_css_selector('#tbody > tr > td > a')
congressmanName = td_a[0].text
td_a[0].click()
# congressmans = []
# for a in td_a:
#     congressmans.append(a.text)
#     # print(a.text)
# print(congressmans)
# 의원 이름 수집

driver.implicitly_wait(3)
javaScript = 'javascript:openPopup();'
driver.execute_script(javaScript)
window_before = driver.window_handles[0]
window_after = driver.window_handles[1]
driver.switch_to_window(window_after)
# 의원정보 popup창 열고 handler 이동

politicalParty = ''
politicalRegion = ''
belongingAgency = ''
congressmanInformations = driver.find_elements_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd')
# politicalParty = driver.find_element_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(2)')
politicalParty = congressmanInformations[0].text
politicalRegion = congressmanInformations[1].text
belongingAgency = congressmanInformations[2].text

congressmanDict = dict(name = congressmanName, party = politicalParty, region = politicalRegion, agency = belongingAgency)
congressmans.append(congressmanDict)
print(congressmans)

driver.implicitly_wait(3)
close = driver.find_element_by_css_selector('#contentMain > div.name_title > a').click()

driver.switch_to_window(window_before)
# driver.find_element_by_css_selector('#pageListViewArea2 > a:nth-child(2)').click()
# region = driver.find_element_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(4)')

driver.back()
# driver.quit()
