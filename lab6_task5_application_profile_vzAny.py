import requests
import json
from pprint import pprint
requests.packages.urllib3.disable_warnings()


USERNAME = 'admin'
PASSWORD = '1234QWer'
URL = 'https://192.168.10.1/'

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

# create bridge domain for DNSany
BD_NAME = 'APILAB-GUI-DNS-BD'
GATEWAY = '192.168.144.254/24'
TENANT = 'APILAB-GUI'
VRF = 'APILAB-GUI-VRF'

payload_bd = {
    'fvBD': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/BD-{BD_NAME}',
            'mac': '00:22:BD:F8:19:FF',
            'arpFlood': 'true',
            'name': BD_NAME,
            'rn': f'BD-{BD_NAME}',
            'status': 'created'
            },
        'children': [
            {'fvSubnet': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/BD-{BD_NAME}/subnet-[{GATEWAY}]',
                    'ctrl': '',
                    'ip': GATEWAY,
                    'preferred': 'true',
                    'rn': f'subnet-[{GATEWAY}]',
                    'status': 'created'},
                'children': []
                }
            },
            {'fvRsCtx': {
                'attributes': {
                    'tnFvCtxName': VRF,
                    'status': 'created,modified'},
                'children': []
                }
            }
            ]
    }
}

result_bd = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/BD-{BD_NAME}.json', data=json.dumps(payload_bd), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_bd.status_code))
pprint(result_bd.content)

# create contract
FILTER = 'DNS'
CONTRACT_NAME = 'DNSany'
SUBJECT_NAME = 'DNS'

payload_contr = {
    'vzBrCP': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}',
            'name': CONTRACT_NAME,
            'rn': f'brc-{CONTRACT_NAME}',
            'status': 'created'},
        'children': [
            {'vzSubj': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/brc-{CONTRACT_NAME}/subj-{SUBJECT_NAME}',
                    'name': SUBJECT_NAME,
                    'rn': f'subj-{SUBJECT_NAME}',
                    'status': 'created'},
                'children':[
                    {'vzRsSubjFiltAtt': {
                        'attributes': {
                            'status': 'created,modified',
                            'tnVzFilterName': FILTER,
                            'directives': 'none'},
                        'children':[]}}
                    ]}}
            ]}
}

result_contr = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/brc-{CONTRACT_NAME}.json', data=json.dumps(payload_contr), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_contr.status_code))
pprint(result_contr.content)

# create access profile
AP_NAME = 'DNS'
EPG_NAME = 'DNS_EPG'

payload_ap = {
    'fvAp': {
        'attributes': {
            'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}',
            'name': AP_NAME,
            'rn': f'ap-{AP_NAME}',
            'status': 'created'},
        'children': [
            {'fvAEPg': {
                'attributes': {
                    'dn': f'uni/tn-{TENANT}/ap-{AP_NAME}/epg-{EPG_NAME}',
                    'name': EPG_NAME,
                    'rn': f'epg-{EPG_NAME}',
                    'status': 'created'},
                'children': [
                    {'fvRsBd': {
                        'attributes': {
                            'tnFvBDName': BD_NAME,
                            'status': 'created,modified'},
                        'children':[]
                        }
                    },
                    {'fvRsProv': {
                        'attributes': {
                            'tnVzBrCPName': CONTRACT_NAME,
                            'status': 'created,modified'},
                        'children':[]
                        }
                    }
                    ]
                }
            }
        ]
    }
}

result_ap = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP_NAME}.json', data=json.dumps(payload_ap), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_ap.status_code))
pprint(result_ap.content)

# vzANY
payload_vzany = {
    'vzRsAnyToCons': {
        'attributes': {
            'tnVzBrCPName': CONTRACT_NAME,
            'status': 'created'},
        'children': []
    }
}

result_vzany = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ctx-{VRF}/any.json', data=json.dumps(payload_vzany), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_vzany.status_code))
pprint(result_vzany.content)
