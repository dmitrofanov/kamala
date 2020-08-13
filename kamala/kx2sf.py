import json


import math

import logging

from kx import *

from sf import *

def flush_api_table(api_endpoint, table_name, starting_offset=0):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    r = get_data_chunk(api_endpoint, starting_offset)

    ctx = connect()

    logging.info(f"Deleting table data: " + table_name)
    del_from_table(ctx, table_name)

    total_count = r.get("total_count")
    count = r.get("count")


    total_pages = math.ceil((total_count-starting_offset)/count)

    logging.info(f"Start processing, total_pages:{total_pages}, total_count: {total_count}, count: {count})")
    for x in range(total_pages):
        try:
            logging.info(f"Requesting page {x} of {total_pages}")
            r = get_data_chunk(api_endpoint, str(starting_offset + count*x))
            logging.info(f"Writing page {x} of {total_pages} to SnowFlake")

            mrg_to_table(ctx, table_name, r)

            logging.info(f"Page {x} of {total_pages} loaded")
        except:
            logging.exception(api_endpoint + str(starting_offset + count*x) + f"Page {x} of {total_pages} failed")

    ctx.close()

def flush_kamala_appointments(starting_offset=0):
    flush_api_table(API_VISIT, TABLE_VISIT, starting_offset)

def flush_kamala_appointments2(starting_offset=0):
    flush_api_table(API_APPOINTMENTS2, TABLE_APPOINTMENTS2, starting_offset)

def flush_kamala_order_detail():
    #flush_api_table(API_APPOINTMENTS2, TABLE_APPOINTMENTS2, starting_offset)
    logging.basicConfig(filename='example.log',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    table_name = TABLE_ORDER_DETAIL

    ctx = connect()
    cs = ctx.cursor()

    logging.info(f"Deleting table data: " + table_name)
    del_from_table(ctx, table_name)

    for appointment_id, rn, cnt in cs.execute("select appointment_id, row_number() over (order by appointment_id) rn, count(*) over () cnt from (select distinct appointment_id from vkamala_order)"):
        try:
            logging.info(f"Requesting page {rn} of {cnt}")
            logging.info(f"order_id: {appointment_id}")
            response = get_data_chunk(API_ORDER_DETAIL, appointment_id)
            logging.info(f"Writing page {rn} of {cnt} to SnowFlake")
            mrg_to_table(ctx, table_name, response)
            logging.info(f"Page {rn} of {cnt} loaded")
        except:
            logging.exception(API_ORDER_DETAIL + str(appointment_id) + f"Page {rn} of {cnt} failed")

    ctx.close()

#def flush_kamala_appointments():
#    flush_api_table("https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset=", 'KAMALA_APPOINTMENTS')