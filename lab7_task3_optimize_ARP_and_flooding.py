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
BD = 'APILAB-bare'

payload_task = {
    'fvBD': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD}',
            'unkMacUcastAct': 'proxy',
            'arpFlood': 'false'
        },
        'children': []
        }
}

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
