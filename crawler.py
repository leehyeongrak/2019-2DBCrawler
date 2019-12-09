import requests
from bs4 import BeautifulSoup as bs
import re # 공백 문자(\r\n\t)를 제거하기 위한 모듈
import json

# >>> 의원의 소속 기관의 데이터까지 수집해야 하는 경우
def crawlCongressManDataUsingRequestFromPopup():
    congressManList = []
    count = 0
    url = 'http://likms.assembly.go.kr/bill/memVoteResult.do#'
    soup = bs(requests.get(url).text, 'html.parser')
    congressMan = soup.select('#tbody > tr > td > a')
    for man in congressMan:
        picDeptCd = man['href'].split('\'')[1]
        openPopupUrl = 'http://www.assembly.go.kr/assm/memPop/memPopup.do?dept_cd={0}'.format(picDeptCd)
        eachSoup = bs(requests.get(openPopupUrl).text, 'html.parser')
        if eachSoup.select('title')[0].text != '400 Bad Request':
            name = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.left > div > h4')[0].text
            party = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(2)')[0].text
            region = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(4)')[0].text
            agency = eachSoup.select('#contentMain > div.cont_in > div.info_mna > ul > li.right > dl > dd:nth-child(6)')[0].text
            regex = re.compile(r'[\n\r\t]')
            agency = regex.sub('', agency)
            agency = agency.split(' ')[0]
            manInfo = {
                'congressManCode': picDeptCd,
                'congressManName': name,
                'party': party,
                'region': region,
                'committeeName': agency
            }
            congressManList.append(manInfo)
            count += 1
            print(manInfo)
            print(count)
        else:
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
                'picDeptCd': picDeptCd
            })
            eachSoup = bs(eachPage.text, 'html.parser')
            agency = ''
            manInfo = {
                'congressManCode': picDeptCd,
                'congressManName': eachSoup.select_one('p.lang01').text,
                'party': eachSoup.select_one('div.personInfo > dl > dd:nth-child(2)').text,
                'region': eachSoup.select_one('div.personInfo > dl > dd:nth-child(4)').text,
                'committeeName': agency
            }
            congressManList.append(manInfo)
            count += 1
            print(manInfo)
            print(count)
    jsonDict = {'data': congressManList}
    with open('congressMan.json', 'w', encoding='utf-8') as f:
        json.dump(jsonDict, f, ensure_ascii=False)


# >>> 한 회차에 대한 모든 의안 데이터 수집
def crawlBillData(sessionCd, currentsCd, currentsDt, billList):
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
        'tabMenuType': 'billVoteResult',
        'searchYn': 'ABC'
    })
    jsonData = json.loads(eachPage.text)
    for bill in jsonData['resListVo']:
        billInfo = {
            'billCode': bill['billno'],
            'billName': bill['billname'],
            'processDate': bill['processdate'],
            'committeeName': bill['currcommitte'],
            "agree": bill['agree'],
            "withdraw": bill['withdraw'],
            "disagree": bill['disagree'],
            "billResult": bill['result']
        }
        billList.append(billInfo)


# >>> 20대 국회 모든 회차에 대한 의안 데이터 수집
def crawlBillDataFromEachSession():
    billList = []
    url = 'http://likms.assembly.go.kr/bill/billVoteResult.do'
    soup = bs(requests.get(url).text, 'html.parser')
    divs = soup.select('#ageListDiv > a')
    for div in divs:
        splits = div['onclick'].split('\'')
        sessionCd = splits[3]
        currentsCd = splits[5]
        currentsDt = splits[7]
        crawlBillData(sessionCd, currentsCd, currentsDt, billList)
    jsonDict = {'data': billList}
    with open('bill.json', 'w', encoding='utf-8') as f:
        json.dump(jsonDict, f, ensure_ascii=False)


# >>> 한 회차에 있는 모든 의안에 대한 모든 의원의 찬반 데이터 수집
def crawlConfirmData(sessionCd, currentsCd, currentsDt, confirmList):
    url = 'http://likms.assembly.go.kr/bill/memVoteResult.do#'
    soup = bs(requests.get(url).text, 'html.parser')
    congressMan = soup.select('#tbody > tr > td > a')
    for man in congressMan:
        picDeptCd = man['href'].split('\'')[1]
        eachPage = requests.post('http://likms.assembly.go.kr/bill/memVoteResultDetailAjax.do', data={
            'ageFrom': 20,
            'ageTo': 20,
            'age': 20,
            'sessionCd': sessionCd,
            'currentsCd': currentsCd,
            'currentsDt': currentsDt,
            'orderColumn': 'ProposeDt',
            'orderType': 'ASC',
            'strPage': 1,
            'pageSize': 1000,
            'maxPage': 10,
            'allCount': 75,
            'tabMenuType': 'billVoteResult',
            'picDeptCd': picDeptCd,
            'tabMenuType': 'billVoteResult',
            'searchYn': 'Y',
            'searchKind': '전체'
        })
        jsonData = json.loads(eachPage.text)
        for confirm in jsonData['resListVo']:
            confirmInfo = {
                'congressManCode': picDeptCd,
                'billCode': confirm['billNo'],
                "resultVote": confirm['resultVote']
            }
            confirmList.append(confirmInfo)


# >>> 모든 회차에 있는 모든 의안에 대한 모든 의원의 찬반 데이터 수집
def crawlConfirmDataFromEachSession():
    confirmList = []
    url = 'http://likms.assembly.go.kr/bill/billVoteResult.do'
    soup = bs(requests.get(url).text, 'html.parser')
    divs = soup.select('#ageListDiv > a')
    count = 0
    for div in divs:
        if count == 10:
            break
        splits = div['onclick'].split('\'')
        sessionCd = splits[3]
        currentsCd = splits[5]
        currentsDt = splits[7]
        crawlConfirmData(sessionCd, currentsCd, currentsDt, confirmList)
        count = count + 1
    jsonDict = {'data': confirmList}
    with open('confirm.json', 'w', encoding='utf-8') as f:
        json.dump(jsonDict, f, ensure_ascii=False)
