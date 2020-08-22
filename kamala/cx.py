import requests
import json
import math
import logging


# CX - ClientiX
CX_ENDPOINT = "https://klientiks.ru/clientix/Restapi/"

API_ACCOUNT = '390b96e2763e'
API_USER = 'd969c9cde78c'
API_TOKEN = '073de5009f21b34afa022cfa7ca2c124'

# ACL - Appointment Client Links
API_ACL_NAME = 'ACL'
API_ACL_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="

# REACL = RoistatExportACL
API_REACL_NAME = 'REACL'
API_REACL_LINK = CX_ENDPOINT + "roistatExportAcl/a/{}/u/{}/t/{}/ik/orders/rvwk/status,statuses/?date=1521871200&offset="

# CLDT - CLient by DaTe
API_CLDT_NAME = 'CLDT'
API_CLDT_LINK = CX_ENDPOINT + "list/a/{}/u/{}/t/{}/m/clients/date/"

# GA - Get Appointment
API_GA_NAME = 'GA'
API_GA_LINK = CX_ENDPOINT + "getAppointment/a/{}/u/{}/t/{}/id/"

API = {API_ACL_NAME: API_ACL_LINK,
       API_REACL_NAME: API_REACL_LINK,
       API_CLDT_NAME: API_CLDT_LINK,
       API_GA_NAME: API_GA_NAME}



def get_api_link(api_name, page):
    return API[api_name].format(API_ACCOUNT, API_USER, API_TOKEN) + page


def get_data_chunk(api_name, offset=""):
    api_link = get_api_link(api_name, str(offset))
    logging.debug(f'Requesting data chunk {api_link}')
    r = requests.get(url=(api_link))
    return r.text


def get_pages(api_name, offset=""):
    if api_name == API_ACL_NAME:
        l_offset = 0 if offset == "" else int(offset)
        logging.info(f'Get pages {API_ACL_NAME} offset {l_offset}')
        r = get_data_chunk(api_name, l_offset)
        total_count = int(r["total_count"]) - l_offset
        count = int(r["count"])
        pages = math.ceil(total_count / count)
        logging.info(f'Original total count {r["total_count"]}, altered total count {total_count}, count {count}, pages {pages}')
    #elif api_name == 
        #return map(lambda x: l_offset + count * --x, range(pages))


def get_chunks(api_name, offset=""):
    return map(lambda x: get_data_chunk(api_name, x), get_pages(api_name, offset))

#def push_acl():
    #r = get_data_chunk(api_name, l_offset)