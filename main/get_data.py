from bs4 import BeautifulSoup
import json, asyncio, os, aiohttp
import lxml, requests
from config import *
url='https://kursksu.ru/pages/rating_bak_spec_budget_2023'
import requests
response = requests.get(url=url, cookies=cookies, headers=headers)
soup=BeautifulSoup(response.text,'lxml')
def  get_data():
    table=soup.find_all('div', class_='panel panel-default')
    for i in table:
        data={}
        name=i.find('a').text.strip()
        if ('очная бюджет' in name) and not 'заочная' in name:
            name=name.replace('/', '_').replace(':', ' -')[:-13]
            data.update({'Направление':name})
            m = i.find('p').find_next('p').find_next('p').text.split()
            m = str(m[2])[:-1]
            data.update({'Места':m})
            dat=i.find('table', class_='table table-striped table-bordered').find_all('tr')
            user_data={}
            count1=0
            count2=0
            for j in dat[5:]:
                st=j.find_all('td')
                nam=st[0].text
                snils=st[1].text
                priorety=st[9].text
                sm=st[2].text
                doc=st[11].text
                user={
                    "Номер": nam,
                    "Сумма баллов":  sm,
                    'Приоритет':  priorety,
                    'Документ': doc}
                user_data.update({snils: user})
                if doc=='Оригинал':
                    count2+=1
                    user.update({'Место в списке оригиналов': count2})
                else:user.update({'Место в списке оригиналов': count2})
                if (priorety=='1') and doc=='Оригинал':
                    count1+=1
                    user.update({'Место в списке: оригинал+высший приоритет': count1})
                else:user.update({'Место в списке: оригинал+высший приоритет': count1})
            data.update({"Конкурс": user_data})
            with open(f'data/{name}.json', 'w', encoding='utf-8-sig') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        else: continue
def main():
    get_data()
if __name__ == '__main__':
    main()