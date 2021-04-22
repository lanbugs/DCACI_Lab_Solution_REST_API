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
TENANT_NAME = 'APILAB-GUI'
TENANT_VRF_NAME = 'APILAB-GUI-VRF'

payload_task = {
    'fvTenant' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT_NAME}',
            'name': TENANT_NAME,
            'rn': f'tn-{TENANT_NAME}',
            'status': 'created',
        },
        'children': [
        {'fvCtx': {
            'attributes': {
                'dn': f'uni/tn-{TENANT_NAME}/ctx-{TENANT_VRF_NAME}',
                'name': TENANT_VRF_NAME,
                'rn': f'ctx-{TENANT_VRF_NAME}',
                'status': 'created'
            },
            'children': []
        }}
        ]
    }
}

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT_NAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
