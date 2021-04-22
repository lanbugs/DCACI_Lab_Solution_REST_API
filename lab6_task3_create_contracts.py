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

# 2. task
TENANT = 'APILAB-GUI'

CONTRACTS = [
    {'name': 'web_contract',
     'scope': 'application-profile',
     'subjects': [
         {'name': 'http',
          'filter': 'http'},
         {'name': 'https',
          'filter': 'https'}
     ]},
    {'name': 'db_contract',
     'scope': 'application-profile',
     'subjects': [
         {'name': 'mysql',
          'filter': 'mysql'}
     ]},
    {'name': 'app_contract',
     'scope': 'application-profile',
     'subjects': [
         {'name': 'tomcat',
          'filter': 'tomcat'}
     ]},

]

for contract in CONTRACTS:

    CONTRACT_NAME = contract['name']
    CONTRACT_SCOPE = contract['scope']

    CONTRACT_CHILDS = []

    for subject in contract['subjects']:
        SUBJECT_NAME = subject['name']
        SUBJECT_FILTER = subject['filter']
        sub_child = {'vzSubj': {
                        'attributes': {
                            'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}/subj-{SUBJECT_NAME}',
                            'name': SUBJECT_NAME,
                            'rn': f'subj-{SUBJECT_NAME}',
                            'status': 'created'
                        },
                        'children': [ {
                            'vzRsSubjFiltAtt': {
                                'attributes': {
                                    'status': 'created,modified',
                                    'tnVzFilterName': SUBJECT_FILTER,
                                    'directives': 'none'
                                },
                                'children': []
                                }
                        }
                        ]
                    }
        }

        CONTRACT_CHILDS.append(sub_child)

    payload_task = {
        'vzBrCP': {
            'attributes': {
                'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}',
                'name': CONTRACT_NAME,
                'scope': CONTRACT_SCOPE,
                'rn': f'brc-{CONTRACT_NAME}',
                'status': 'created'
            },
            'children': CONTRACT_CHILDS
        }
    }

    result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/brc-{CONTRACT_NAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result.status_code))
    pprint(result.content)
