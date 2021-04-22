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

# create baremetal bridge domain
TENANT = 'APILAB-GUI'
BD = 'APILAB-bare'
VRF = 'APILAB-GUI-VRF'


payload_task_bd = {
    'fvBD' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD}',
            'name': BD,
            'arpFlood': 'true',
            'unkMacUcastAct': 'flood',
            'unicastRoute': 'false',
            'rn': f'BD-{BD}',
            'status': 'created',
        },
        'children': [
            {'fvRsCtx': {
                'attributes': {
                    'tnFvCtxName': VRF,
                    'status': 'created,modified'
                },
                'children': []
                }
            }
        ]
    }
}

result_bd = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD}.json', data=json.dumps(payload_task_bd), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_bd.status_code))
pprint(result_bd.content)

# create app profile
AP_NAME = 'APILAB-bare'
EPG_NAME = 'APILAB-bare-EPG'
PHY_DOM = 'APILAB-bare-DOM'
LEAF_ID = '101'
POD_ID = '1'
INTERFACE = '1/14'
VLAN = '240'

payload_task_ap_epg = {
    'fvAp' : {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}',
            'name': AP_NAME,
            'rn': f'ap-{AP_NAME}',
            'status': 'created',
        },
        'children': [ 
            {'fvAEPg': {       
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}/epg-{EPG_NAME}',
                    'name': EPG_NAME,
                    'rn': f'epg-{EPG_NAME}',
                    'status': 'created'
                },
                'children': [
                    {'fvRsPathAtt': {
                        'attributes': {
                            'tDn': f'topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{INTERFACE}]',
                            'encap': f'vlan-{VLAN}',
                            'status': 'created'
                        }, 'children': []}},
                    {'fvRsBd': {
                        'attributes': {
                            'tnFvBDName': BD,
                            'status': 'created,modified'
                        }, 'children': []}},
                    {'fvRsDomAtt': {
                        'attributes': {
                            'tDn': f'uni/phys-{PHY_DOM}',
                            'status': 'created'
                        }, 'children': []}},
                ]
                }
            }
        
        ]
    }
}

result_ap_epg = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}.json', data=json.dumps(payload_task_ap_epg), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ap_epg.status_code))
pprint(result_ap_epg.content)


# Add second path
POD_ID = '1'
LEAF_ID = '102'
INTERFACE = '1/14'

payload_task_secp = {
    'fvRsPathAtt' : {
        'attributes': {
            'tDn': f'topology/pod-{POD_ID}/paths-{LEAF_ID}/pathep-[eth{INTERFACE}]',
            'encap': f'vlan-{VLAN}',
            'instrImedcy': 'immediate',
            'mode': 'untagged',
            'status':'created',
        },
        'children': []
    }
}

result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}/epg-{EPG_NAME}.json', data=json.dumps(payload_task_secp), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result.status_code))
pprint(result.content)


