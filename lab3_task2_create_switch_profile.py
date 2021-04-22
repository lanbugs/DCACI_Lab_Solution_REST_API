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

LEAF_PROFILE_NAME = 'APILAB-Leaf-101'
LEAF_NODE_ID = "101"
LEAF_101_NAME = 'APILAB-Leaf-101'
LEAF_101_102_NAME = 'APILAB-Leaf-101-102'
NODE_BLOCK_NAME = "Leaf-101" # you can use any name must only be unique in profile

LEAF_101 = {
	'attributes': {
		'tDn': f'uni/infra/accportprof-{LEAF_101_NAME}',
		'status': 'created,modified'
	},
	'children': []
}

LEAF_101_102 = {
	'attributes': {
		'tDn': f'uni/infra/accportprof-{LEAF_101_102_NAME}',
		'status': 'created,modified'
	},
	'children': []
}

payload_task = {
	'infraNodeP': {
		'attributes': {
			'dn': f'uni/infra/nprof-{LEAF_PROFILE_NAME}',
			'name': LEAF_PROFILE_NAME,
			'status': 'created,modified'
		},
		'children': [
				{
					'infraLeafS': {
						'attributes': {
							'dn': f'uni/infra/nprof-{LEAF_PROFILE_NAME}/leaves-{LEAF_PROFILE_NAME}-typ-range',
							'type': 'range',
							'name': LEAF_PROFILE_NAME,
							'rn': f'leaves-{LEAF_PROFILE_NAME}-typ-range',
							'status': 'created'
						},
						'children': [ { 
							'infraNodeBlk': {
								'attributes': {
									'dn': f'uni/infra/nprof-{LEAF_PROFILE_NAME}/leaves-{LEAF_PROFILE_NAME}-typ-range/nodeblk-{NODE_BLOCK_NAME}',
									'from_': LEAF_NODE_ID,
									'to_': LEAF_NODE_ID,
									'name': NODE_BLOCK_NAME,
									'rn': f'nodeblk-{NODE_BLOCK_NAME}',
									'status': 'created'
								},
								"children": []
							}
						}
					]
					}
				},
				{
					'infraRsAccPortP': LEAF_101
				},
				{
					'infraRsAccPortP': LEAF_101_102
				}
				]
			}
	}


result = requests.post(f'{URL}api/node/mo/uni/infra/nprof-{LEAF_PROFILE_NAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)


