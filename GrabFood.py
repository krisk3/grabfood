import requests
import pandas as pd
import re

headers = {
    'authority': 'portal.grab.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://food.grab.com',
    'referer': 'https://food.grab.com/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-country-code': 'PH',
    'x-gfc-country': 'PH',
    'x-grab-web-app-version': '7JxnV__dTfJZAKF80UUJO',
    'x-hydra-jwt': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnYWEiLCJhdWQiOiJnZnciLCJuYW1lIjoiZ3JhYnRheGkiLCJpYXQiOjE2ODQxNTY5NTgsImV4cCI6MTY4NDE1NzU1OCwibmJmIjoxNjg0MTU2OTU4LCJ2ZXIiOiIxLjE5LjAuMjQiLCJicklEIjoiNDliYjllMDI5NGJmNTViZGRhMzg5ODNjOTMzNWNjNTdiYTB5NnIiLCJzdXMiOmZhbHNlLCJicklEdjIiOiIxMDRhOTczZjc0NjgzZTk4ZWY3ZDNjNjYxMzNmODA1OWUyN3k2ciIsImJyVUlEIjoiMGY1OGNiMTktNWJiYy00YWI5LTk4OTEtMDk3MTMwMzI5ODMwIn0.K3x9JOXJS2jRB-VLZWfYavLdud8tUbcmZKbRr2mxtDFXp2OFT6xo33dT7UyEMoTsogVa4g4L7_DEWQMaBbKVATMm8vbo9-RislT2Jg62D4_Fu32vCE9ygtP_Nj0HWEkCnZozpwpBvIscwNd7UKf7fIcvX79fTq7ctXwSU-daXA_RwycBsmLLsornnVldDkXqhbfYr2hAGwnSV_tHK468xqjPaQRbOOxzCHZd65G04t9q3n_aaYLslKRHns3NiThq8HfE0tzzQ5paWkZqBkuVDhqS6OWvAqGtLsyllOuu2b8ZC3yRLYRe4MqVDXsVa22AqkYdu2zrPmvMHyJW2QyJpw',
    'x-recaptcha-token': '03AL8dmw8QXz3FwnHjUpJ8IaGW1uf_EHknB69AS0t9TuszjUl2AdfrOr6hwnalWauNgCnz8_wi_jajRluSQJ1RzQwvfQa4J97syzLClJxwiK6bTWbpUrvJbdVCtc2Unk5sMhuUOaIBJAYXAMiuFerPJxsAeiQafZIZto9940J75gQEtqLrsLn7D5u11sdplJOBQLxkvtv5La0arpTqpT296A7tDo8mMJ9ZYr1GHGUX-tzIWwO3_6U18Bx9CgUP4BoKr1qsFY0MBlA3kN-ubLW5jBpbFFivEI2B3kzVeDaAqOa81LOcI8uq5466JPxVS_iTnfuvkrvMNCIYInlFPdTwXyKJYKVHyLWqymA-zFvF2DlhaeZ5y0tixxdapoBQwYjTfott7CAua7unHZAbr2Stv0kwLSI0vpYLvxXucCtVHVkCjMNyJ3EzzJ1NuaAVvU3I_6uAp4kpfqHO3wvfddfk1PVC9x1FvixkAbYThgqxisa1bPlITEc__I5Y-mB4nmihklCGlb5y577ThNTJtxZo_-wkAZUFAw1XaGMhUxM9PWtyXVqE7CklV4o',
}


json_data = {
        'latlng': '14.514129098091843,120.98080039623011',
        'keyword': '',
        'offset': 0,
        'pageSize': 32,
        'countryCode': 'PH',
    }
response = requests.post('https://portal.grab.com/foodweb/v2/search', headers=headers, json=json_data).json()
no_of_res = response['searchResult']['totalCount']
no_of_res = int((no_of_res/32)+1)

j = 0
data = []
for i in range(no_of_res):
    json_data = {
        'latlng': '14.514129098091843,120.98080039623011',
        'keyword': '',
        'offset': j,
        'pageSize': 32,
        'countryCode': 'PH',
    }

    response = requests.post('https://portal.grab.com/foodweb/v2/search', headers=headers, json=json_data).json()
    for merchant in response['searchResult']['searchMerchants']:
        res_dict = {}
        res_name = merchant['address']['name']
        res_dict['Restaurant Name'] = re.sub(r'\[.*?\]', '', res_name)
        res_dict['Latitude'] = merchant['latlng']['latitude']
        res_dict['Longitude'] = merchant['latlng']['longitude']
        data.append(res_dict)
        
    j += 32
    
df = pd.DataFrame(data)
df.to_csv('GrabFood.xls', index=False)
