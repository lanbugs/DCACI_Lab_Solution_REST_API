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

# create contract
TENANT = 'APILAB-GUI'
AP = 'APILAB-bare'
SRC_EPG = 'APILAB-bare-EPG'
DST_EPG = 'APILAB-bare2-EPG'
CONTRACT_NAME = 'myfirstcontract'

payload_task = {
    'fvTenant' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT}',
            'status': 'modified',
        },
        'children': [
            {'fvAp': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/ap-{AP}',
                    'status': 'modified'
                }, 
                'children': [
                    {'fvAEPg': {
                        'attributes': {
                            'dn': f'uni/tn-{TENANT}/ap-{AP}/epg-{SRC_EPG}',
                            'status': 'modified'
                        },
                        'children': [
                            {'fvRsProv': {
                                'attributes': {
                                    'tnVzBrCPName': CONTRACT_NAME,
                                    'status': 'created,modified'
                                },
                                'children': []}}]
                            }},
                    {'fvAEPg': {
                        'attributes': {
                            'dn': f'uni/tn-{TENANT}/ap-{AP}/epg-{DST_EPG}',
                            'status': 'modified'
                            },
                        'children': [
                            {'fvRsCons': {
                                'attributes': {
                                    'tnVzBrCPName': CONTRACT_NAME,
                                    'status': 'created,modified'
                                }, 'children': []}},
                            ]
                        }
                    }
                ]
                }
            },
            {'vzBrCP': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}',
                    'scope': 'tenant',
                    'name': CONTRACT_NAME,
                    'status': 'created'
                    },
                'children': [
                    {'vzSubj': {
                        'attributes': {
                            'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}/subj-Subject',
                            'name': 'Subject',
                            'status': 'created'
                        }, 
                        'children': [
                            {'vzRsSubjFiltAtt': {
                                'attributes': {
                                    'tnVzFilterName': 'default',
                                    'status': 'created,modified'
                                }, 
                                'children': []}}, 
                                                ]}},

                                        ]}},
                    ]
                }
    }

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
