import json
#библиотека для получения HTML кода страницы
import requests
#библиотека для парсинга HTML доков
from bs4 import BeautifulSoup



MPTurl = 'https://mpt.ru/studentu/raspisanie-zanyatiy'
#создание переменной, которая содержит в себе код страницы мпт
MPTurlContent = requests.get(MPTurl)

#даем доступ библиотеке к HTML коду сайта
soup = BeautifulSoup(MPTurlContent.content, "lxml")

navTabs = soup.find('ul', class_="nav-tabs")
navTabsLinks = navTabs.find_all('a')

navTabsGroups = soup.find_all('div', class_="tab-pane")

specialitys = []


for a in navTabsLinks:
    for group in navTabsGroups:
        if a.get('aria-controls') == group.get('id'):
            navTabsGroupsName = group.find_all('a')
            # print(navTabsGroupsName)
            groups = ", ".join([a.text for a in navTabsGroupsName])
            hrefs = [link.get('href') for link in navTabsGroupsName]
            specialitys.append({
                'id': a.get('aria-controls'),
                'name': a.text,
                'groups': [
                    {
                        'parentId': a.get('aria-controls'),
                        'groups': groups,
                        'id': hrefs
                    }
                ]
            })
            break

# ensure_ascii = False - запрещает преобразование в юникод
specialitysJSON = json.dumps(specialitys, indent = 2, ensure_ascii = False)
# print(specialitysJSON)



def search_speciality():
    searchSpecialyty = input('введите специальность:').strip()
    for speciality in specialitys:
        if searchSpecialyty.lower() in speciality['name'].lower():
            print(json.dumps(speciality, indent=2, ensure_ascii=False))
            break
        else:
            continue


# search_speciality()

# def search_group():
#     searchGroup = input('введите группу:').strip()
#     for groupInfo in specialitys['groups']:
#        if any(searchGroup.lower() in group.lower() for group in groupInfo['groups']):
#            print(json.dumps(groupInfo, indent=2, ensure_ascii=False))
#            break
#        else:
#            continue
#
#
# search_group()