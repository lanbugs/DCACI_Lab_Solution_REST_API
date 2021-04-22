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

INTERFACE_PROFILE_NAME = "APILAB-Leaf-101"

payload_task = {
	'infraAccPortP': {
		'attributes': {
			'dn': f'uni/infra/accportprof-{INTERFACE_PROFILE_NAME}',
			'name': INTERFACE_PROFILE_NAME,
			'rn': f'accportprof-{INTERFACE_PROFILE_NAME}',
			'status': 'created,modified'
			},
		'children': []
		}
}

result = requests.post(f'{URL}api/node/mo/uni/infra/accportprof-{INTERFACE_PROFILE_NAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
