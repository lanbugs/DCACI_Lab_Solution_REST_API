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

# CDP interface profile
CDP_PROFILE_NAME = 'APILAB-CDP-ON'

payload_task_cdp = {
	'cdpIfPol': {
		'attributes': {
			'dn': f'uni/infra/cdpIfP-{CDP_PROFILE_NAME}',
			'name': CDP_PROFILE_NAME,
			'rn': f'cdp-IfP-{CDP_PROFILE_NAME}',
			'status': 'created'
		},
		'children': []
	}
}

result_cdp = requests.post(f'{URL}api/node/mo/uni/infra/cdpIfP-{CDP_PROFILE_NAME}.json', data=json.dumps(payload_task_cdp), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_cdp.status_code))
pprint(result_cdp.content)

# LLDP RX-TX
LLDP_PROFILE_NAME = 'APILAB-LLDP-TX-RX'

payload_task_lldp = {
	'lldpIfPol': {
		'attributes': {
			'dn': f'uni/infra/lldpIfP-{LLDP_PROFILE_NAME}',
			'name': LLDP_PROFILE_NAME,
			'rn': f'lldpIfP-{LLDP_PROFILE_NAME}',
			'status': 'created'
		},
		'children': []
	}
}

result_lldp = requests.post(f'{URL}api/node/mo/uni/infra/lldpIfP-{LLDP_PROFILE_NAME}.json', data=json.dumps(payload_task_lldp), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_lldp.status_code))
pprint(result_lldp.content)


# Portchannel Policy active
LACP_ACTIVE_PROFILE = 'APILAB-LACP-active'

payload_task_lacp_active = {
	'lacpLagPol': {
		'attributes': {
			'dn': f'uni/infra/lacplagp-{LACP_ACTIVE_PROFILE}',
			'name': LACP_ACTIVE_PROFILE,
			'rn': f'lacplagp-{LACP_ACTIVE_PROFILE}',
            'ctrl': 'graceful-conv,fast-sel-hot-stdby',
            'mode': 'active',
			'status': 'created'
		},
		'children': []
	}
}

result_lacp_active = requests.post(f'{URL}api/node/mo/uni/infra/lacplagp-{LACP_ACTIVE_PROFILE}.json', data=json.dumps(payload_task_lacp_active), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_lacp_active.status_code))
pprint(result_lacp_active.content)


# Portchannel Policy active suspendindividual
LACP_ACTIVE_SI_PROFILE = 'APILAB-LACP-active-suspendindividual'

payload_task_lacp_active_si = {
	'lacpLagPol': {
		'attributes': {
			'dn': f'uni/infra/lacplagp-{LACP_ACTIVE_SI_PROFILE}',
			'name': LACP_ACTIVE_SI_PROFILE,
			'rn': f'lacplagp-{LACP_ACTIVE_SI_PROFILE}',
            'mode': 'active',
			'status': 'created'
		},
		'children': []
	}
}

result_lacp_active_si = requests.post(f'{URL}api/node/mo/uni/infra/lacplagp-{LACP_ACTIVE_SI_PROFILE}.json', data=json.dumps(payload_task_lacp_active_si), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_lacp_active_si.status_code))
pprint(result_lacp_active_si.content)

# Portchannel member Policy slow
PO_MEMBER_PROFILE_SLOW = 'APILAB-LACP-slow'

payload_po_member_slow = {
	'lacpIfPol': {
		'attributes': {
			'dn': f'uni/infra/lacpifp-{PO_MEMBER_PROFILE_SLOW}',
            'name': PO_MEMBER_PROFILE_SLOW,
            'rn': f'lacpifp-{PO_MEMBER_PROFILE_SLOW}',
            'status': 'created'
		},
		'children': []
	}
}

result_po_member_slow = requests.post(f'{URL}api/node/mo/uni/infra/lacpifp-{PO_MEMBER_PROFILE_SLOW}.json', data=json.dumps(payload_po_member_slow), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_po_member_slow.status_code))
pprint(result_po_member_slow.content)

# Portchannel member Policy fast
PO_MEMBER_PROFILE_FAST = 'APILAB-LACP-fast'

payload_po_member_fast = {
	'lacpIfPol': {
		'attributes': {
			'dn': f'uni/infra/lacpifp-{PO_MEMBER_PROFILE_FAST}',
            'name': PO_MEMBER_PROFILE_FAST,
            'txRate': 'fast',
            'rn': f'lacpifp-{PO_MEMBER_PROFILE_FAST}',
            'status': 'created'
		},
		'children': []
	}
}

result_po_member_fast = requests.post(f'{URL}api/node/mo/uni/infra/lacpifp-{PO_MEMBER_PROFILE_FAST}.json', data=json.dumps(payload_po_member_fast), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_po_member_fast.status_code))
pprint(result_po_member_fast.content)


#Create STP policy
STP_POLICY_NAME = "APILAB-BPDUguard-enabled"

payload_stp = {
    'stpIfPol' : {
        'attributes': {
            'dn': f'uni/infra/ifPol-{STP_POLICY_NAME}',
            'name': STP_POLICY_NAME,
            'ctrl': 'bpdu-guard',
            'rn': f'ifPol-{STP_POLICY_NAME}',
            'status': 'created'
        },
        'children': []
    }
}

result_stp = requests.post(f'{URL}api/node/mo/uni/infra/ifPol-{STP_POLICY_NAME}.json', data=json.dumps(payload_stp), verify = False, cookies=COOKIES)

print('Return code: {code}'.format(code=result_stp.status_code))
pprint(result_stp.content)
