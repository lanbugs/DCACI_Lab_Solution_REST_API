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

# create vlan pool
POOL_NAME = 'APILAB-bare-VLAN'
VLAN_FROM = '240'
VLAN_TO = '242'

payload_task_vlan_pool = {
    'fvnsVlanInstP' : {
        'attributes': {
            'dn': f'uni/infra/vlanns-[{POOL_NAME}]-static',
            'name': POOL_NAME,
            'allocMode': 'static',
            'rn': f'vlanns-[{POOL_NAME}]-static',
            'status': 'created',
        },
        'children': [ {'fvnsEncapBlk': {
            'attributes': {
                'dn': f'uni/infra/vlanns-[{POOL_NAME}]-static/from-[vlan-{VLAN_FROM}]-to-[vlan-{VLAN_TO}]',
                'from': f'vlan-{VLAN_FROM}',
                'to': f'vlan-{VLAN_TO}',
                'rn': f'from-[vlan-{VLAN_FROM}]-to-[vlan-{VLAN_TO}]',
                'status': 'created'
            },
            'children': []
            }}
        ]
    }
}

result_vlan = requests.post(f'{URL}api/node/mo/uni/infra/vlanns-[{POOL_NAME}]-static.json', data=json.dumps(payload_task_vlan_pool), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_vlan.status_code))
pprint(result_vlan.content)

# create phsical domain
PD_NAME = 'APILAB-bare-DOM'

payload_task_pd = {
    'physDomP' : {
        'attributes': {
            'dn': f'uni/phys-{PD_NAME}',
            'name': PD_NAME,
            'rn': f'phys-{PD_NAME}',
            'status': 'created',
        },
        'children': [{'infraRsVlanNs': {
            'attributes': {
               'tDn': f'uni/infra/vlanns-[{POOL_NAME}]-static',
               'status': 'created'
            },
            'children': []
        }}
        ]
    }
}

result_pd = requests.post(f'{URL}api/node/mo/uni/phys-{PD_NAME}.json', data=json.dumps(payload_task_pd), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_pd.status_code))
pprint(result_pd.content)

# create attachable access entity profile
AAEP_PROFILE = 'APILAB-bare-AAEP'

payload_task_aaep = {
    'infraInfra' : {
        'attributes': {
            'dn': 'uni/infra',
            'status': 'modified',
        },
        'children': [ {'infraAttEntityP': {
            'attributes': {
                'dn': f'uni/infra/attentp-{AAEP_PROFILE}',
                'name': AAEP_PROFILE,
                'rn': f'attentp-{AAEP_PROFILE}',
                'status': 'created',
            },
            'children': [
                {'infraRsDomP': {
                    'attributes': {
                        'tDn': f'uni/phys-{PD_NAME}',
                        'status': 'created'
                    },
                    'children': []
                    }
                },
                {'infraFuncP': {
                    'attributes': {
                        'dn': 'uni/infra/funcprof',
                        'status': 'modified'
                        },
                    'children': []
                    }
                }
                ]
            }    
           }
        ]
    }
}

result_aaep = requests.post(f'{URL}api/node/mo/uni/infra.json', data=json.dumps(payload_task_aaep), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_aaep.status_code))
pprint(result_aaep.content)



# Create Link level policy
LLP_PROFILE = 'APILAB-1G'

payload_task_llp = {
    'fabricHIfPol' : {
        'attributes': {
            'dn': f'uni/infra/hintfpol-{LLP_PROFILE}',
            'name': LLP_PROFILE,
            'speed': '1G',
            'rn': f'hintfpol-{LLP_PROFILE}',
            'status': 'created',
        },
        'children': []
    }
}

result_llp = requests.post(f'{URL}api/node/mo/uni/infra/hintfpol-{LLP_PROFILE}.json', data=json.dumps(payload_task_llp), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_llp.status_code))
pprint(result_llp.content)


# Create interface policy
INTERFACE_POLICY_NAME = 'APILAB-bare1'

payload_task_ifpol = {
    'infraAccPortGrp' : {
        'attributes': {
            'dn': f'uni/infra/funcprof/accportgrp-{INTERFACE_POLICY_NAME}',
            'name': INTERFACE_POLICY_NAME,
            'rn': 'accportgrp-{INTERFACE_POLICY_NAME}',
            'status': 'created'
        },
        'children': [
            {'infraRsHIfPol': {
                'attributes': {
                    'tnFabricHIfPolName': LLP_PROFILE,
                    'status': 'created,modified'
                    },
                'children': []
                }
            },
            {'infraRsAttEntP': {
                'attributes': {
                    'tDn': f'uni/infra/attentp-{AAEP_PROFILE}',
                    'status': 'created,modified'
                },
                'children': []
                }
            }
        ]
    }
}

result_ifpol = requests.post(f'{URL}api/node/mo/uni/infra/funcprof/accportgrp-{INTERFACE_POLICY_NAME}.json', data=json.dumps(payload_task_ifpol), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ifpol.status_code))
pprint(result_ifpol.content)



# Clone to bare2
OLD_INTERFACE = 'APILAB-bare1'
NEW_INTERFACE = 'APILAB-bare2'


# get old profile
old_result = requests.get(f'{URL}api/node/mo/uni/infra/funcprof/accportgrp-{OLD_INTERFACE}.json?rsp-subtree=full&rsp-prop-include=config-only', cookies=COOKIES, verify=False)
old_config = json.loads(old_result.content)['imdata'][0]

# create new profile
new_config = old_config

# set new values
new_config['infraAccPortGrp']['attributes']['name'] = NEW_INTERFACE
new_config['infraAccPortGrp']['attributes']['dn'] = f'uni/infra/funcprof/accportgrp-{NEW_INTERFACE}'
new_config['infraAccPortGrp']['attributes']['rn'] = f'accportgrp-{NEW_INTERFACE}'

result = requests.post(f'{URL}api/node/mo/uni/infra/funcprof/accportgrp-{NEW_INTERFACE}.json', data=json.dumps(new_config), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)


# Attach bare1
ACP_SELECTOR_NAME = 'APILAB-bare1'
LEAF = 'APILAB-Leaf-101'
BLOCK = 'block1'
FROM_PORT = '14'
TO_PORT = '14'

payload_task_ab1 = {
    'infraHPortS' : {
        'attributes': {
            'dn': f'uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range',
            'name': ACP_SELECTOR_NAME,
            'rn': f'hports-{ACP_SELECTOR_NAME}-typ-range',
            'status': 'created,modified',
        },
        'children': [
        {'infraPortBlk': {
            'attributes': {
                'dn': f'uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range/portblk-{BLOCK}',
                'fromPort': FROM_PORT,
                'toPort': TO_PORT,
                'name': BLOCK,
                'rn': f'portblk-{BLOCK}',
                'status': 'created,modified'
            },
            'children': []}},
        {'infraRsAccBaseGrp': {
            'attributes': {
                'tDn': f'uni/infra/funcprof/accportgrp-{ACP_SELECTOR_NAME}',
                'status': 'created,modified'
            },
            'children': []}},
        ]
    }
}

result_ab1 = requests.post(f'{URL}api/node/mo/uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range.json', data=json.dumps(payload_task_ab1), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ab1.status_code))
pprint(result_ab1.content)

# Attach bare2
ACP_SELECTOR_NAME = 'APILAB-bare2'
LEAF = 'APILAB-Leaf-102'
BLOCK = 'block1'
FROM_PORT = '14'
TO_PORT = '14'

payload_task_ab1 = {
    'infraHPortS' : {
        'attributes': {
            'dn': f'uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range',
            'name': ACP_SELECTOR_NAME,
            'rn': f'hports-{ACP_SELECTOR_NAME}-typ-range',
            'status': 'created,modified',
        },
        'children': [
        {'infraPortBlk': {
            'attributes': {
                'dn': f'uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range/portblk-{BLOCK}',
                'fromPort': FROM_PORT,
                'toPort': TO_PORT,
                'name': BLOCK,
                'rn': f'portblk-{BLOCK}',
                'status': 'created,modified'
            },
            'children': []}},
        {'infraRsAccBaseGrp': {
            'attributes': {
                'tDn': f'uni/infra/funcprof/accportgrp-{ACP_SELECTOR_NAME}',
                'status': 'created,modified'
            },
            'children': []}},
        ]
    }
}

result_ab2 = requests.post(f'{URL}api/node/mo/uni/infra/accportprof-{LEAF}/hports-{ACP_SELECTOR_NAME}-typ-range.json', data=json.dumps(payload_task_ab1), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ab2.status_code))
pprint(result_ab1.content)
