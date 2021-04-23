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

# configure mac address

TENANT = 'APILAB-GUI'
BD = 'APILAB-bare'
MAC = '00:00:0c:9f:f0:00'

payload_mac = {
    'fvBD': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD}',
            'mac': MAC
        },
        'children': []
        }
}

result_mac = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD}.json', data=json.dumps(payload_mac), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_mac.status_code))
pprint(result_mac.content)

# configure gateway ip
GATEWAY = '172.17.40.254/24'

payload_gw = {
    'fvSubnet': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD}/subnet-[{GATEWAY}]',
            'ctrl': '',
            'ip': GATEWAY,
            'rn': f'subnet-[{GATEWAY}]',
            'status': 'created'},
        'children': []
        }
}

result_gw = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD}/subnet-[{GATEWAY}].json', data=json.dumps(payload_gw), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_gw.status_code))
pprint(result_gw.content)

# enable unicast routing
payload_uni = {
    'fvBD': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD}',
            'unicastRoute': 'true'
        },
        'children': []
    }
}

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD}.json', data=json.dumps(payload_uni), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)
