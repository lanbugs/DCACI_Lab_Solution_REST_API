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

# create second epg

TENANT = 'APILAB-GUI'
AP = 'APILAB-bare'
EPG_NAME = 'APILAB-bare2-EPG'
BD = 'APILAB-bare'
PHY_DOM = 'APILAB-bare-DOM'
POD_ID = '1'
LEAF_ID = '102'
INTERFACE = '1/14'
VLAN = '240'

payload_task = {
    'fvAEPg' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP}/epg-{EPG_NAME}',
            'name': EPG_NAME,
            'rn': f'epg-{EPG_NAME}',
            'status': 'created',
        },
        'children': [
            {'fvRsBd': {
                'attributes': {
                    'tnFvBDName': BD,
                    'status': 'created,modified'
                },
                'children': []}},
            {'fvRsDomAtt': {
                'attributes': {
                    'tDn': f'uni/phys-{PHY_DOM}',
                    'status': 'created'
                }, 'children': []}},
            {'fvRsPathAtt': {
                'attributes': {
                    'tDn': f'topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{INTERFACE}]',
                    'instrImedcy': 'immediate',
                    'mode': 'untagged',
                    'encap': f'vlan-{VLAN}',
                    'status': 'created'
                }, 'children': []}},
        ]
    }
}

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP}/epg-{EPG_NAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)



# delete static port from other epg
TENANT = 'APILAB-GUI'
AP = 'APILAB-bare'
EPG_NAME = 'APILAB-bare-EPG'
POD_ID = '1'
LEAF_ID = '102'
INTERFACE = '1/14'


payload_task_d = {
    'fvRsPathAtt' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP}/epg-{EPG_NAME}/rspathAtt-[topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{INTERFACE}]]',
            'status': 'deleted'
        },
        'children': []
    }
}

result_d = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP}/epg-{EPG_NAME}/rspathAtt-[topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{INTERFACE}]].json', data=json.dumps(payload_task_d), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_d.status_code))
pprint(result_d.content)
