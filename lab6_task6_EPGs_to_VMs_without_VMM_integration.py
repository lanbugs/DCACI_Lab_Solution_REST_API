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

# create vlan pool
VLAN_NAME = 'APILAB-nonintegrated-VLAN'
VLAN_FROM = '340'
VLAN_TO = '349'

payload_vlan = {
    'fvnsVlanInstP': {
        'attributes': {
            'dn': f'uni/infra/vlanns-[{VLAN_NAME}]-static',
            'name': VLAN_NAME,
            'allocMode': 'static',
            'rn': f'vlanns-[{VLAN_NAME}]-static',
            'status': 'created'
            },
        'children': [
            {'fvnsEncapBlk': {
                'attributes': {
                    'dn': f'uni/infra/vlanns-[{VLAN_NAME}]-static/from-[vlan-{VLAN_FROM}]-to-[vlan-{VLAN_TO}]',
                    'from': f'vlan-{VLAN_FROM}',
                    'to': f'vlan-{VLAN_TO}',
                    'rn': f'from-[vlan-{VLAN_FROM}]-to-[vlan-{VLAN_TO}]',
                    'status': 'created'
                },
                'children': []
            }
        }
    ]
    }
}

result_v = requests.post(f'{URL}api/node/mo/uni/infra/vlanns-[{VLAN_NAME}]-static.json', data=json.dumps(payload_vlan), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_v.status_code))
pprint(result_v.content)

# create phsical domain
PHY_DOM_NAME = 'APILAB-nonintegrated-DOM'

payload_pd = {
    'physDomP': {
        'attributes': {
            'dn': f'uni/phys-{PHY_DOM_NAME}',
            'name': PHY_DOM_NAME,
            'rn': f'phys-{PHY_DOM_NAME}',
            'status': 'created'
        },
        'children': [
            {'infraRsVlanNs': {
                'attributes': {
                    'tDn': f'uni/infra/vlanns-[{VLAN_NAME}]-static',
                    'status': 'created'
                },
                'children': []
                }
            }
        ]
    }
}

result_pd = requests.post(f'{URL}api/node/mo/uni/phys-{PHY_DOM_NAME}.json', data=json.dumps(payload_pd), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_pd.status_code))
pprint(result_pd.content)

# create AAEP profile for ESXi1 and 2
AAEP_NAME = 'APILAB-vSphere-AAEP'
VPC_ESXi1_POLICY_GROUP = 'APILAB-ESXi-1'
VPC_ESXi2_POLICY_GROUP = 'APILAB-ESXi-2'

payload_aaep = {
    'infraInfra': {
        'attributes': {
            'dn':'uni/infra',
            'status':'modified'
        },
        'children': [
            {'infraAttEntityP': {
                'attributes': {
                    'dn': f'uni/infra/attentp-{AAEP_NAME}',
                    'name': AAEP_NAME,
                    'rn': f'attentp-{AAEP_NAME}',
                    'status': 'created'},
                'children': [
                    {'infraRsDomP': {
                        'attributes': {
                            'tDn': f'uni/phys-{PHY_DOM_NAME}',
                            'status': 'created'
                        },
                        'children': []
                        }
                    }
                ]
            }
            },
            {'infraFuncP': {
                'attributes': {
                    'dn': 'uni/infra/funcprof',
                    'status': 'modified'
                },
                'children': [
                    {'infraAccBndlGrp': {
                        'attributes': {
                            'dn': f'uni/infra/funcprof/accbundle-{VPC_ESXi1_POLICY_GROUP}',
                            'status': 'modified'
                        },
                        'children': [
                            {'infraRsAttEntP': {
                                'attributes': {
                                    'tDn': f'uni/infra/attentp-{AAEP_NAME}',
                                    'status': 'created,modified'
                                },
                                'children': []
                            }
                            }
                        ]
                    }
                    },
                    {'infraAccBndlGrp': {
                        'attributes': {
                            'dn': f'uni/infra/funcprof/accbundle-{VPC_ESXi2_POLICY_GROUP}',
                            'status': 'modified'
                        },
                        'children': [
                            {'infraRsAttEntP': {
                                'attributes': {
                                    'tDn': f'uni/infra/attentp-{AAEP_NAME}',
                                    'status': 'created,modified'
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
        ]
    }
}

result_aaep = requests.post(f'{URL}api/node/mo/uni/infra.json', data=json.dumps(payload_aaep), verify = False, cookies=COOKIES)
print('Return code: {code}'.format(code=result_aaep.status_code))
pprint(result_aaep.content)

# create deploy VPC tagged vlan interface
VPC_TO_EPGS = [
    {'epg': 'web_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '341',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-1'
     },
    {'epg': 'web_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '341',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-2'
     },
    {'epg': 'app_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '342',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-1'
     },
    {'epg': 'app_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '342',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-2'
     },
    {'epg': 'db_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '343',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-1'
     },
    {'epg': 'db_EPG',
     'ap': '3-Tier-App',
     'tenant': 'APILAB-GUI',
     'vlan': '343',
     'pod': '1',
     'path': '101-102',
     'pathep': 'APILAB-ESXi-2'
     },

]

for element in VPC_TO_EPGS:

    EPG = element['epg']
    AP = element['ap']
    TENANT = element['tenant']
    VLAN = element['vlan']
    POD = element['pod']
    PATH = element['path']
    PATHEP = element['pathep']

    payload = {
        'fvRsPathAtt': {
            'attributes': {
                'encap': f'vlan-{VLAN}',
                'instrImedcy': 'immediate',
                'tDn': f'topology/pod-{POD}/protpaths-{PATH}/pathep-[{PATHEP}]',
                'status': 'created'
            },
            'children': []
        }
    }

    result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP}/epg-{EPG}.json',
                           data=json.dumps(payload), verify=False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result.status_code))
    pprint(result.content)


# associate web_EPG to phsical BD
EPGS_TO_PHYBD = [
    {
        'epg': 'web_EPG',
        'ap': '3-Tier-App',
        'phy_dom': 'APILAB-nonintegrated-DOM',
        'tenant': 'APILAB-GUI'
    },
    {
        'epg': 'app_EPG',
        'ap': '3-Tier-App',
        'phy_dom': 'APILAB-nonintegrated-DOM',
        'tenant': 'APILAB-GUI'
    },
    {
        'epg': 'db_EPG',
        'ap': '3-Tier-App',
        'phy_dom': 'APILAB-nonintegrated-DOM',
        'tenant': 'APILAB-GUI'
    },

]

for element in EPGS_TO_PHYBD:
    EPG = element['epg']
    AP = element['ap']
    PHY_DOM_NAME = element['phy_dom']
    TENANT = element['tenant']

    payload = {
        'fvRsDomAtt': {
            'attributes': {
                'resImedcy': 'immediate',
                'tDn': f'uni/phys-{PHY_DOM_NAME}',
                'status': 'created'
            },
            'children': []
        }
    }

    result = requests.post(f'{URL}api/node/mo/uni/tn-{TENANT}/ap-{AP}/epg-{EPG}.json', data=json.dumps(payload), verify = False, cookies=COOKIES)

    print('Return code: {code}'.format(code=result.status_code))
    pprint(result.content)
