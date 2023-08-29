from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.common import exceptions

def iselement(browser,xpaths):
    try:
        browser.find_element_by_xpath(xpaths)
        return browser.find_element_by_xpath(xpaths).text
    except exceptions.NoSuchElementException:
        return ""

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_argument("disable-cache")
options.add_argument('log-level=3')

driver = webdriver.Chrome(chrome_options=options,executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")

start_url = 'https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E9%9B%86%E6%88%90%E6%88%98%E7%95%A5%E5%85%B3%E5%8D%A1'

driver.get(start_url)
time.sleep(3)

mission_name = driver.find_element_by_xpath('//div[@class="mw-category-group"]').text
mission_name_list = mission_name.split('\n')
del mission_name_list[0]


for ms_name in mission_name_list:
    info_mission = {}
    info_name = ms_name
    info_mission['Mission_name'] = info_name
    ms_name = ms_name.replace(' ', '_')
    next_url = u'http://prts.wiki/w/{}'.format(ms_name)
    print(next_url)
    driver.get(next_url)
    time.sleep(1)
    info_mission['Place'] = driver.find_element_by_xpath(
            '//table[@class="wikitable"][1]/tbody/tr[7]/td[1]').text
    info_mission['Cost'] = driver.find_element_by_xpath('//table[@class="wikitable"][1]/tbody/tr[7]/td[2]').text
    info_mission['Max_cost'] = driver.find_element_by_xpath('//table[@class="wikitable"][1]/tbody/tr[7]/td[3]').text
    info_mission['Blood'] = driver.find_element_by_xpath('//table[@class="wikitable"][1]/tbody/tr[9]/td[1]').text
    info_mission['Enemy_count'] = driver.find_element_by_xpath('//table[@class="wikitable"][1]/tbody/tr[9]/td[2]').text
    info_mission['Min_time'] = driver.find_element_by_xpath('//table[@class="wikitable"][1]/tbody/tr[9]/td[3]').text
    info_mission['Detail'] = iselement(driver,'//table[@class="wikitable"][1]/tbody/tr[10]/td')
    info_mission['Place_em'] = iselement(driver,'//table[@class="wikitable"][2]/tbody/tr[7]/td[1]')
    info_mission['Cost_em'] = iselement(driver,'//table[@class="wikitable"][2]/tbody/tr[7]/td[2]')
    info_mission['Max_cost_em'] = iselement(driver,'//table[@class="wikitable"][2]/tbody/tr[7]/td[3]')
    info_mission['Detail_em'] = iselement(driver,'//table[@class="wikitable"][2]/tbody/tr[8]/td')

    item = driver.find_element_by_xpath("//table[@class='wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible']").text
    item = item.split('\n')
    item = item[3:-1]
    new_dict = {}
    for i in range(len(item)):
        item_1 = item[i].split(' ')
        if len(item_1) == 14:
            del item_1[0]
        new_dict[item_1[0]] = {}
        new_dict[item_1[0]]['count'] = item_1[1]
        new_dict[item_1[0]]['status'] = item_1[2]
        new_dict[item_1[0]]['level'] = item_1[3]
        new_dict[item_1[0]]['hp'] = item_1[4]
        new_dict[item_1[0]]['atk'] = item_1[5]
        new_dict[item_1[0]]['def'] = item_1[6]
        new_dict[item_1[0]]['res'] = item_1[7]
        new_dict[item_1[0]]['atk_dis'] = item_1[8]
        new_dict[item_1[0]]['weitght'] = item_1[9]
        new_dict[item_1[0]]['speed'] = item_1[10]
        new_dict[item_1[0]]['atkr'] = item_1[11]
        new_dict[item_1[0]]['de_blood'] = item_1[12]
        

    info_mission['Enemy_info'] = new_dict
    del new_dict
    
    print(info_mission)

    way = 'info/{}.json'.format(ms_name)
    with open(way,'w',encoding='utf-8-sig') as f:
        line = json.dumps(dict(info_mission),indent=4,ensure_ascii=False)
        f.write(line)
    time.sleep(1)
    break #测试用 爬取请注释此行
driver.quit()
