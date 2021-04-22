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

# Create interface policy
INTERFACE_POLICY_NAME = 'APILAB-ESXi-1'
LACP_POLICY = 'APILAB-LACP-active'
CDP_POLICY = 'APILAB-CDP-ON'
LLDP_POLICY = 'APILAB-LLDP-TX-RX'
STP_POLICY = 'APILAB-BPDUguard-enabled'

payload_task_ifpol = {
    'infraAccBndlGrp' : {
        'attributes': {
            'dn': f'uni/infra/funcprof/accbundle-{INTERFACE_POLICY_NAME}',
            'lagT': 'node',
            'name': INTERFACE_POLICY_NAME,
            'rn': 'accbundle-{INTERFACE_POLICY_NAME}',
            'status': 'created'
        },
        'children': [
            {'infraRsLacpPol': {
                'attributes': {
                    'tnLacpLagPolName': LACP_POLICY,
                    'status': 'created,modified'
                    },
                'children': []
                }
            },
            {'infraRsCdpIfPol': {
                'attributes': {
                    'tnCdpIfPolName': CDP_POLICY,
                    'status': 'created,modified'
                },
                'children': []
                }
            },
            {'infraRsLldpIfPol': {
                'attributes': {
                    'tnLldpIfPolName': LLDP_POLICY,
                    'status': 'created,modified'
                },
                'children': []
                }
            },
            {'infraRsStpIfPol': {
                'attributes': {
                    'tnStpIfPolName': STP_POLICY,
                    'status': 'created,modified'
                },
                'children': []
                }
            },
        ]
    }
}

result_ifpol = requests.post(f'{URL}api/node/mo/uni/infra/funcprof/accbundle-{INTERFACE_POLICY_NAME}.json', data=json.dumps(payload_task_ifpol), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ifpol.status_code))
pprint(result_ifpol.content)

# Attach policy to interface
LEAF_INTERFACE_PROFILE = 'APILAB-Leaf-101-102'
INTERFACE_POLICY_GROUP = 'APILAB-ESXi-1'
ACCESS_GROUP = 'APILAB-ESXi-1'
PORT_BLOCK = 'block1'
INTERFACE = '4'

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
