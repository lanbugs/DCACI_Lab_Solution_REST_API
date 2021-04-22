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
payload_task = {
    '' : {
        'attributes': {
            'dn': f'',
            'name':,
            'rn': f'',
            'status':,
        },
        'children': []
    }
}

result = requests.post(f'{URL}api/node/mo/uni/infra/lacpifp-{PO_MEMBER_PROFILE_FAST}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
