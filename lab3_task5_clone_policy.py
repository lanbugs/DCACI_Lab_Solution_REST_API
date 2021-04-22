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
OLD_PROFILE = 'APILAB-ESXi-1'
NEW_PROFILE = 'APILAB-ESXi-2'

# get old profile
old_result = requests.get(f'{URL}api/node/mo/uni/infra/funcprof/accbundle-{OLD_PROFILE}.json?rsp-subtree=full&rsp-prop-include=config-only', cookies=COOKIES, verify=False)
old_config = json.loads(old_result.content)['imdata'][0]

# create new profile
new_config = old_config

# set new values
new_config['infraAccBndlGrp']['attributes']['name'] = NEW_PROFILE
new_config['infraAccBndlGrp']['attributes']['dn'] = f'uni/infra/funcprof/accbundle-{NEW_PROFILE}'
new_config['infraAccBndlGrp']['attributes']['rn'] = f'accbundle-{NEW_PROFILE}'

result = requests.post(f'{URL}api/node/mo/uni/infra/funcprof/accbundle-{NEW_PROFILE}.json', data=json.dumps(new_config), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)


# Create access port selector for ESXi-2
LEAF_INTERFACE_PROFILE = 'APILAB-Leaf-101-102'
INTERFACE_POLICY_GROUP = 'APILAB-ESXi-2'
ACCESS_GROUP = 'APILAB-ESXi-2'
PORT_BLOCK = 'block1'
INTERFACE = '34'

payload_task_attach_policy = {
    'infraHPortS' : {
        'attributes': {
            'dn': f'uni/infra/accportprof-{LEAF_INTERFACE_PROFILE}/hports-{INTERFACE_POLICY_GROUP}-typ-range',
            'name': INTERFACE_POLICY_GROUP,
            'rn': f'hports-{INTERFACE_POLICY_GROUP}-typ-range',
            'status': 'created,modified',
        },
        'children': [
            {'infraPortBlk': {
                'attributes': {
                    'dn': f'uni/infra/accportprof-{LEAF_INTERFACE_PROFILE}/hports-{INTERFACE_POLICY_GROUP}-typ-range/portblk-{PORT_BLOCK}',
                    'name': PORT_BLOCK,
                    'fromPort': INTERFACE,
                    'toPort': INTERFACE,
                    'rn': f'portblk-{PORT_BLOCK}',
                    'status': 'created,modified'
                },
                'children': []
                }
            },
            {'infraRsAccBaseGrp': {
                'attributes': {
                    'tDn': f'uni/infra/funcprof/accbundle-{ACCESS_GROUP}',
                    'status': 'created,modified' 
                },
                'children': []
                }
            }
        ]
    }
}

result_attach_pol = requests.post(f'{URL}api/node/mo/uni/infra/accportprof-{LEAF_INTERFACE_PROFILE}/hports-{INTERFACE_POLICY_GROUP}-typ-range.json', data=json.dumps(payload_task_attach_policy), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_attach_pol.status_code))
pprint(result_attach_pol.content)
