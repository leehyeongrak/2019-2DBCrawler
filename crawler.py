import requests
from bs4 import BeautifulSoup as bs
# from selenium import webdriver
import re
# >>> 공백 문자(\r\n\t)를 제거하기 위한 모듈
import json
# >>> 의안 데이터의 request 반환 형식이 json이기 때문에

# def crawlCongressManDataUsingRequestFromPopup():
#     url = 'http://likms.assembly.go.kr/bill/memVoteResult.do#'
#     soup = bs(requests.get(url).text, 'html.parser')
#     congressMan = soup.select('#tbody > tr > td > a')
#     for man in congressMan:
#         picDeptCd = man['href'].split('\'')[1]
#         openPopupUrl = 'http://www.assembly.go.kr/assm/memPop/memPopup.do?dept_cd={0}'.format(picDeptCd)
#         eachSoup = bs(requests.get(openPopupUrl).text, 'html.parser')
#
#         if eachSoup.select('title')[0].text != '400 Bad Request':
#             name = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.left > div > h4')[0].text
#             party = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(2)')[0].text
#             region = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(4)')[0].text
#             agency = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(6)')[0].text
#             regex = re.compile(r'[\n\r\t]')
#             agency = regex.sub('', agency)
#
#             manInfo = {
#                 'name': name,
#                 'party': party,
#                 'region': region,
#                 'agency': agency
#             }
#             print(manInfo)

def crawlCongressManDataUsingRequest():
    url = 'http://likms.assembly.go.kr/bill/memVoteResult.do#'
    soup = bs(requests.get(url).text, 'html.parser')
    congressMan = soup.select('#tbody > tr > td > a')
    print(congressMan)
    for man in congressMan:
        eachPage = requests.post('http://likms.assembly.go.kr/bill/memVoteDetail.do', data={
            'ageFrom': 20,
            'ageTo': 20,
            'age': 20,
            'orderColumn': 'ProposeDt',
            'orderType': 'ASC',
            'strPage': 1,
            'pageSize': 10,
            'maxPage': 10,
            'tabMenuType': 'billVoteResult',
            'searchYn': '전체',
            'picDeptCd': man['href'].split('\'')[1]
        })
        eachSoup = bs(eachPage.text, 'html.parser')
        manInfo = {
            'name': eachSoup.select_one('p.lang01').text,
            'party': eachSoup.select_one('div.personInfo > dl > dd:nth-child(2)').text,
            'region': eachSoup.select_one('div.personInfo > dl > dd:nth-child(4)').text
        }
        print(manInfo)
# crawlCongressManDataUsingRequest()

def crawlBillData(sessionCd, currentsCd, currentsDt):
    # >>> 의안 데이터는 json 형식으로 긁어옴
    url = 'http://likms.assembly.go.kr/bill/billVoteResultListAjax.do'
    eachPage = requests.post(url, data={
        'ageFrom': 20,
        'ageTo': 20,
        'age': 20,
        'sessionCd': sessionCd,
        'currentsCd': currentsCd,
        'currentsDt': currentsDt,
        'orderType': 'ASC',
        'strPage': 1,
        'pageSize': 1000,
        'maxPage': 10,
        'allCount': 88,
        'tabMenuType': 'billVoteResult',
        'searchYn': 'ABC'
    })
    jsonData = json.loads(eachPage.text)
    for bill in jsonData['resListVo']:
        billInfo = {
            'billno': bill['billno'],
            'billname': bill['billname'],
            'processdate': bill['processdate'],
            'currcommitte': bill['currcommitte'],
            "agree": bill['agree'],
            "withdraw": bill['withdraw'],
            "disagree": bill['disagree'],
            "result": bill['result']
        }
        print(billInfo)
        print('\n')
    # billno, billname, processdate, currcommitte

    # parsed = json.loads(eachPage.text)
    # dumps = json.dumps(parsed, ensure_ascii = False, indent=4, sort_keys=True)
    # print(dumps)

crawlBillData(371, 11, 20191119)
crawlBillData(371, 10, 20191031)
# sessionCd: 371
# currentsCd: 10
# currentsDt: 20191031









# >>> Selenium 크롤링
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
#
# driver = webdriver.Chrome('/Users/rak/Python/chromedriver', chrome_options=options)
# >>> headless로 드라이버 실행
#
# driver = webdriver.Chrome('/Users/rak/Python/chromedriver')
# driver.implicitly_wait(3)
# # >>> 크롬 드라이버 생성 및 데이터의 완전한 로딩을 위한 3초 기다림
#
# driver.get('http://likms.assembly.go.kr/bill/memVoteResult.do#')
# # >>> url 실행
#
# congressmans = []
# # congressmanName = ''
# # td_a = driver.find_element_by_css_selector('#tbody > tr:nth-child(1) > td:nth-child(1) > a')
# # td_a = driver.find_elements_by_css_selector('#tbody > tr > td > a')
# # congressmanName = td_a[0].text
# # td_a[0].click()
#
# for i in range(319):
#     td_a = driver.find_elements_by_css_selector('#tbody > tr > td > a')
#     congressmanName = td_a[i].text
#     td_a[i].click()
#
#     driver.implicitly_wait(3)
#     javaScript = 'javascript:openPopup();'
#     driver.execute_script(javaScript)
#     window_before = driver.window_handles[0]
#     window_after = driver.window_handles[1]
#     driver.switch_to_window(window_after)
#     # 의원정보 popup창 열고 handler 이동
#
#     politicalParty = ''
#     politicalRegion = ''
#     belongingAgency = ''
#     congressmanInformations = driver.find_elements_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd')
#     # politicalParty = driver.find_element_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(2)')
#     politicalParty = congressmanInformations[0].text
#     politicalRegion = congressmanInformations[1].text
#     belongingAgency = congressmanInformations[2].text
#
#     congressmanDict = dict(name = congressmanName, party = politicalParty, region = politicalRegion, agency = belongingAgency)
#     congressmans.append(congressmanDict)
#     print(congressmans)
#
#     driver.implicitly_wait(3)
#     close = driver.find_element_by_css_selector('#contentMain > div.name_title > a').click()
#
#     driver.switch_to_window(window_before)
#     # driver.find_element_by_css_selector('#pageListViewArea2 > a:nth-child(2)').click()
#     # region = driver.find_element_by_css_selector('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(4)')
#
#     driver.back()
#     driver.implicitly_wait(3)
# # driver.quit()
