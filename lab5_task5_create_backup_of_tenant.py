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

# create snapshot of tenant

DESCRIPTION = 'Lab5 end'
TARGET_TENANT = 'APILAB-GUI'

payload_task = {
    'configExportP' : {
        'attributes': {
            'dn': 'uni/fabric/configexp-defaultOneTime',
            'name': 'defaultOneTime',
            'rn': 'configexp-defaultOneTime',
            'snapshot': 'true',
            'targetDn': f'uni/tn-{TARGET_TENANT}',
            'adminSt': 'triggered',
            'descr': DESCRIPTION,
            'status': 'created,modified',
        },
        'children': []
    }
}

result = requests.post(f'{URL}api/node/mo/uni/fabric/configexp-defaultOneTime.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
