import requests
from scrapy.http import HtmlResponse
import json
import mysql.connector

import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(filename='app2.log',level=logging.INFO,format = '%(name)s - %(asctime)s - %(levelname)s - %(message)s')
# logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
# file_handler = logging.FileHandler('logs/modulelogs.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

import requests

cookies = {
    '_gcl_au': '1.1.1903465340.1677922097',
    '_gid': 'GA1.2.927245461.1677922097',
    'twk_idm_key': '2r_P1mD3bmMO_xNsZRkmM',
    '_ga': 'GA1.2.550806242.1677922097',
    '_gat_gtag_UA_186883065_1': '1',
    'TawkConnectionTime': '0',
    'twk_uuid_5f984696aca01a1688362e64': '%7B%22uuid%22%3A%221.1hGyWtjPibD1Wu490SqgZRAVc8NmMBUoU04bBatWoKNxgmSA8jxfuWGlmtIfqj3VxnDhh8jCdLLtmWKqCHUTI0V8uh6inUxQJsN7H4bXrOpv5GQ5GgC%22%2C%22version%22%3A3%2C%22domain%22%3A%22ineuron.ai%22%2C%22ts%22%3A1677922168986%7D',
    '_ga_5RFEH1BMWX': 'GS1.1.1677922097.1.1.1677922200.0.0.0',
}

headers = {
    'authority': 'ineuron.ai',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_gcl_au=1.1.1903465340.1677922097; _gid=GA1.2.927245461.1677922097; twk_idm_key=2r_P1mD3bmMO_xNsZRkmM; _ga=GA1.2.550806242.1677922097; _gat_gtag_UA_186883065_1=1; TawkConnectionTime=0; twk_uuid_5f984696aca01a1688362e64=%7B%22uuid%22%3A%221.1hGyWtjPibD1Wu490SqgZRAVc8NmMBUoU04bBatWoKNxgmSA8jxfuWGlmtIfqj3VxnDhh8jCdLLtmWKqCHUTI0V8uh6inUxQJsN7H4bXrOpv5GQ5GgC%22%2C%22version%22%3A3%2C%22domain%22%3A%22ineuron.ai%22%2C%22ts%22%3A1677922168986%7D; _ga_5RFEH1BMWX=GS1.1.1677922097.1.1.1677922200.0.0.0',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

def get_product_category():
    response = requests.get('https://ineuron.ai/courses', cookies=cookies, headers=headers)
    xp = HtmlResponse(url='my url',body=response.content)
    row_data = xp.xpath('//*[@type="application/json"]/text()').get('').strip()
    data = json.loads(row_data)
    category_list = data["props"]["pageProps"]["initialState"]["init"]["categories"]
    # print(category)
    # print(type(category))
    # print(len(category))
    for value in category_list.values():
        category = value['title']
        sub_list = value['subCategories']
        for sub_cat in sub_list.values():
            sub_category = sub_cat['title']
            conn = mysql.connector.connect(user='root',host='localhost',password='MyLocal@pass@8155',database='ineuron_data')
            mycurson = conn.cursor(buffered=True)
            mycurson.execute(f"insert into category_list values(default,'{category}','{sub_category}')")
            conn.commit()
            conn.close()

        



def get_product_data():
    response = requests.get('https://ineuron.ai/courses', cookies=cookies, headers=headers)
    xp = HtmlResponse(url='my url',body=response.content)
    row_data = xp.xpath('//*[@type="application/json"]/text()').get('').strip()
    data = json.loads(row_data)
    course_list = data["props"]["pageProps"]["initialState"]["init"]["courses"]
    category = data["props"]["pageProps"]["initialState"]["init"]["categories"]
    # print(course_list)
    print(len(course_list))
    for key,value in course_list.items():
        sub_category = key.replace('"','').replace("'","")

        course_link = f"https://ineuron.ai/course/{sub_category.replace(' ','-')}".replace('"','').replace("'","")
        try:
            tags = value['tags'][0]
            tags = 1 if tags == 'live' else 0
        except:tags=0
        description = value['description'].replace('"','').replace("'","")
        try:start_date = str(value['classTimings']['startDate']).replace('"','').replace("'","")
        except:start_date = 'N/A'
        try:class_timing = str(value['classTimings']['timings']).replace('"','').replace("'","")
        except:class_timing='N/A'
        try:doubt_timing = str(value['classTimings']['doubtClearing']).replace('"','').replace("'","")
        except:doubt_timing ='N/A'
        try:price_IN = str(value['pricing']['IN'])
        except:price_IN = 'N/A'
        try:price_US = str(value['pricing']['US'])
        except:price_US = 'N/A'
        img = value['img']
        print(sub_category)
        print(description)
        

        conn = mysql.connector.connect(user='root',host='localhost',password='MyLocal@pass@8155',database='ineuron_data')
        mycurson = conn.cursor(buffered=True)
        mycurson.execute(f'''insert into course_details values(default,"{sub_category}","{tags}","{description}","{img}","{start_date}","{class_timing}","{doubt_timing}","{price_IN}","{price_US}","{course_link}")''')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    get_product_data()