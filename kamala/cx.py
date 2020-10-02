import requests
import json
import logging
import time


# CX - ClientiX
CX_ENDPOINT = "https://klientiks.ru/clientix/Restapi/"

API_ACCOUNT = '390b96e2763e'
API_USER = 'd969c9cde78c'
API_TOKEN = '073de5009f21b34afa022cfa7ca2c124'

# ACL - Appointment Client Links
API_ACL_NAME = 'ACL'
API_ACL_LINK = CX_ENDPOINT + \
    "list/a/{}/u/{}/t/{}/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="

# REACL = RoistatExportACL
API_REACL_NAME = 'REACL'
API_REACL_LINK = CX_ENDPOINT + \
    "roistatExportAcl/a/{}/u/{}/t/{}/ik/orders/rvwk/status,statuses/?date=1521871200&offset="

# CLDT - CLient by DaTe
API_CLDT_NAME = 'CLDT'
API_CLDT_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/clients/date/"

# GA - Get Appointment
API_GA_NAME = 'GA'
API_GA_LINK = CX_ENDPOINT + "getAppointment/a/{}/u/{}/t/{}/id/"

API_USR_NAME = 'USR'
API_USR_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/Users/?offset="

API_CLT_NAME = 'CLT'
API_CLT_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/clients/?offset="

API_SVC_NAME = 'SVC'
API_SVC_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/Services/?offset="

API = {API_ACL_NAME: API_ACL_LINK,
       API_REACL_NAME: API_REACL_LINK,
       API_CLDT_NAME: API_CLDT_LINK,
       API_GA_NAME: API_GA_NAME,
       API_USR_NAME: API_USR_LINK,
       API_CLT_NAME: API_CLT_LINK,
       API_SVC_NAME: API_SVC_LINK}


def get_api_link(api_name, page):
    return API[api_name].format(API_ACCOUNT, API_USER, API_TOKEN) + str(page)


def get_data_chunk(api_name, offset=""):
    api_link = get_api_link(api_name, str(offset))
    logging.info(f'Requesting data chunk {api_link}')
    r = requests.get(url=(api_link))
    return r.text


def get_chunks(api_name, continue_expr):
    offset = str(0)
    chunk = get_data_chunk(api_name, offset)
    parsed_chunk = json.loads(chunk)
    do_continue = continue_expr(parsed_chunk)
    while do_continue:
        if api_name in (API_USR_NAME, API_SVC_NAME, API_CLT_NAME):
            logging.info(f'Removing JSON parts for {api_name}')
            for i in parsed_chunk["items"]:
                i.pop('json_data', None)
                i.pop('multi_image', None)
                i.pop('multi_file', None)
                i.pop('client_memo', None)
        file_name = f'{api_name}_{offset}'
        yield json.dumps(parsed_chunk), file_name
        offset = str(int(offset) + 50)
        chunk = get_data_chunk(api_name, offset)
        parsed_chunk = json.loads(chunk)
        do_continue = continue_expr(parsed_chunk)
        time.sleep(1)  # Clientix API limits
