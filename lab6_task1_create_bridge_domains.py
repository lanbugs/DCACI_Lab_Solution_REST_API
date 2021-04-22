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
tasks = {}

tasks['web'] = {
    'TENANT': 'APILAB-GUI',
    'BD': 'APILAB-GUI-web-BD',
    'VRF': 'APILAB-GUI-VRF',
    'IP': '192.168.141.254/24'
}

tasks['app'] = {
    'TENANT': 'APILAB-GUI',
    'BD': 'APILAB-GUI-app-BD',
    'VRF': 'APILAB-GUI-VRF',
    'IP': '192.168.142.254/24'
}

tasks['db'] = {
    'TENANT': 'APILAB-GUI',
    'BD': 'APILAB-GUI-db-BD',
    'VRF': 'APILAB-GUI-VRF',
    'IP': '192.168.143.254/24'
}

for key, value in tasks.items():

    TENANT = value['TENANT']
    BD = value['BD']
    VRF = value['VRF']
    IP = value['IP']

    payload_task = {
        'fvTenant' : {
            'attributes': {
                'dn': f'uni/tn-{TENANT}',
                'status': 'modified'
            },
            'children': [
                {'fvBD': {
                    'attributes': {
                        'dn': f'uni/tn-{TENANT}/BD-{BD}',
                        'mac': '00:22:BD:F8:19:FF',
                        'name': BD,
                        'rn': f'BD-{BD}',
                        'status': 'created'
                    },
                    'children': [
                        {'fvRsCtx': {
                            'attributes': {
                                'tnFvCtxName': VRF,
                                'status': 'created,modified'
                            }, 'children': []}},
                        {'fvSubnet': {
                            'attributes': {
                                'dn': f'uni/tn-{TENANT}/BD-{BD}/subnet-[{IP}]',
                                'ctrl': '',
                                'ip': IP,
                                'preferred': 'true',
                                'rn': f'subnet-[{IP}]',
                                'status': 'created'
                            }, 'children': []}},
                    ]}},
            ]
        }
    }

    result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)
    print('Block: {key}'.format(key=key))
    print('Return code: {code}'.format(code=result.status_code))
    pprint(result.content)
