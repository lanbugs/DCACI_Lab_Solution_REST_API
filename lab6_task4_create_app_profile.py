import requests
import json
from pprint import pprint
requests.packages.urllib3.disable_warnings()


USERNAME = "admin"
PASSWORD = "1234QWer"
URL = "https://192.168.10.1/"

# 1. Authentication
payload = {
	'aaaUser': {
		'attributes': {
			'name': USERNAME,
            'pwd': PASSWORD
            }
        }
}

auth = requests.post(f'{URL}api/aaaLogin.json', data=json.dumps(payload), verify=False)
COOKIES = auth.cookies

# create application profile
AP_NAME = '3-Tier-App'
TENANT = 'APILAB-GUI'

payload_task_ap = {
    'fvAp': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}',
            'name': AP_NAME,
            'rn': f'ap-{AP_NAME}',
            'status': 'created',
        },
        'children': []
    }
}

result_ap = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}.json', data=json.dumps(payload_task_ap), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ap.status_code))
pprint(result_ap.content)

# create epgs in AP
EPGS = [
    {'name': 'web_EPG',
     'bd': 'APILAB-GUI-web-BD'},
    {'name': 'app_EPG',
     'bd': 'APILAB-GUI-app-BD'},
    {'name': 'db_EPG',
     'bd': 'APILAB-GUI-db-BD'},
]

for epg in EPGS:
    NAME = epg['name']
    BD = epg['bd']

    payload = {
        'fvAEPg': {
            'attributes': {
                'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}/epg-{NAME}',
                'name': NAME,
                'rn': f'epg-{NAME}',
                'status': 'created'},
            'children': [
                {'fvRsBd': {
                    'attributes': {
                        'tnFvBDName': BD,
                        'status': 'created,modified'
                    },
                    'children': []
                }
                }
            ]
        }
    }

    result_epg = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}/epg-{NAME}.json', data=json.dumps(payload),
                              verify=False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result_epg.status_code))
    pprint(result_epg.content)


# add provided contracts
CONTRACTS = [
    {
        'epg': 'db_EPG',
        'contract': 'db_contract'
     },
    {
        'epg': 'web_EPG',
        'contract': 'web_contract'
    }
]

for contract in CONTRACTS:
    EPG = contract['epg']
    CONTR = contract['contract']

    payload = {
        'fvRsProv': {
            'attributes': {
                'tnVzBrCPName': CONTR,
                'status': 'created,modified'
            },
            'children': []
        }
    }

    result_cnt = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}/epg-{EPG}.json',
                               data=json.dumps(payload),
                               verify=False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result_cnt.status_code))
    pprint(result_cnt.content)


TWOWAY_CONTRACTS = [
    {'contract': 'db_contract',
     'consumer': 'app_EPG',
     'provided': 'db_EPG'
     },
    {'contract': 'app_contract',
     'consumer': 'web_EPG',
     'provided': 'app_EPG'
     },
]

for twy_contract in TWOWAY_CONTRACTS:
    CONTR = twy_contract['contract']
    CONSU = twy_contract['consumer']
    PROVI = twy_contract['provided']

    payload_twy = {'fvAp': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}',
            'status': 'modified'
            },
        'children': [
            {'fvAEPg': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}/epg-{CONSU}',
                    'status': 'modified'
                    },
                'children': [
                    {'fvRsCons': {
                        'attributes': {
                            'tnVzBrCPName': CONTR,
                            'status': 'created,modified'
                        },
                        'children': []
                        }
                    }
                ]
            }
            },
            {'fvAEPg': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}/epg-{PROVI}',
                    'status': 'modified'},
                'children': [
                    {'fvRsProv': {
                        'attributes': {
                            'tnVzBrCPName': CONTR,
                            'status': 'created,modified'
                        },
                        'children': []
                    }
                    }
                ]}
            }
        ]}

    }

    result_twy = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}.json',
                               data=json.dumps(payload_twy),
                               verify=False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result_twy.status_code))
    pprint(result_twy.content)
