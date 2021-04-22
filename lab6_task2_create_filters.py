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
TENANT = 'APILAB-GUI'
FILTERS = [
    {
        'name': 'http',
        'rules': [
        {
        'name': 'http',
        'etherT': 'ip',
        'prot': 'tcp',
        'dFromPort': 'http',
        'dToPort': 'http'
        }
        ]
    },
    {
        'name': 'https',
        'rules': [
        {
        'name': 'https',
        'etherT': 'ip',
        'prot': 'tcp',
        'dFromPort': 'https',
        'dToPort': 'https'
        }
        ]
    },   
    {
        'name': 'mysql',
        'rules': [
        {
        'name': 'mysql',
        'etherT': 'ip',
        'prot': 'tcp',
        'sFromPort': '1024',
        'sToPort': '65535',
        'dFromPort': '3306',
        'dToPort': '3306'
        }
        ]
    }, 
    {
        'name': 'ssh',
        'rules': [
        {
        'name': 'ssh',
        'etherT': 'ip',
        'prot': 'tcp',
        'dFromPort': '22',
        'dToPort': '22'
        }
        ]
    }, 
   {
        'name': 'DNS',
        'rules': [
        {
        'name': 'dns-udp',
        'etherT': 'ip',
        'prot': 'udp',
        'dFromPort': '53',
        'dToPort': '53'
        },
        {
        'name': 'dns-tcp',
        'etherT': 'ip',
        'prot': 'tcp',
        'dFromPort': '53',
        'dToPort': '53'
        }
        ]
    },        
]



for flt in FILTERS:

    FNAME = flt['name']

    payload_filter_childs = []

    for rule in flt['rules']:
        
        RNAME = rule['name']
        ETHERT = rule['etherT']
        PROT = rule['prot']
        dFROMP = rule['dFromPort']
        dTOP = rule['dToPort']
        
        
        genfilter = {'vzEntry': {
                'attributes': {
                    'dn': f"uni/tn-{TENANT}/flt-{FNAME}/e-{RNAME}",
                    'name': RNAME,
                    'etherT': ETHERT,
                    'prot': PROT,
                    'dFromPort': dFROMP,
                    'dToPort': dTOP,
                    'rn': f"e-{RNAME}",
                    'status': 'created,modified'},
                "children":[]
                }
            }
            
        if 'sToPort' in rule.keys():
            sTOP = rule['sToPort']
            genfilter['sToPort'] = sTOP
            
        if 'sFromPort' in rule.keys():
            sFROMP = rule['sFromPort']
            genfilter['sFromPort'] = sFROMP

        
        payload_filter_childs.append(genfilter)


    payload_task = {
        'vzFilter' : {
            'attributes': {
                'dn': f'uni/tn-APILAB-GUI/flt-{FNAME}',
                'name': FNAME,
                'rn': f'flt-{FNAME}',
                'status': 'created,modified',
            },
            'children': [ payload_filter_childs ]
        }
    }

    result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/flt-{FNAME}.json', data=json.dumps(payload_task), verify = False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result.status_code))
    pprint(result.content)
