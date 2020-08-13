#!/usr/bin/env python
import snowflake.connector
import json
import requests

API_APPOINTMENTS = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/AppointmentClientLinks/ik/orders/rvwk/status,statuses/?date=10&offset="
TABLE_APPOINTMENTS = 'KAMALA_APPOINTMENTS'

API_APPOINTMENTS2 = "https://klientiks.ru/clientix/Restapi/roistatExportAcl/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/ik/orders/rvwk/status,statuses/?date=1521871200&offset="
TABLE_APPOINTMENTS2 = 'KAMALA_APPOINTMENTS2'

API_CLIENTS = "https://klientiks.ru/clientix/Restapi/list/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/m/clients/date/"
TABLE_CLIENTS = "KAMALA_CLIENTS"

API_APPOINTMENT_DETAILED = "https://klientiks.ru/clientix/Restapi/getAppointment/a/390b96e2763e/u/d969c9cde78c/t/073de5009f21b34afa022cfa7ca2c124/id/"
TABLE_APPOINTMENT_DETAILED = "KAMALA_APPOINTMENT_DETAILED"

def get_data_chunk(api_endpoint, offset="0"):
    r = requests.get(url=(api_endpoint + str(offset)))
    r.encoding = 'utf-8'
    response = json.loads(r.text)
    return response

def connect():
    # Opens a connection

    ctx = snowflake.connector.connect(
        user='dmitry.mitrofanov',
        password='o22Dm1trof@nova',
        account='ringcentral',
        warehouse='RCUSERS_WH',
        database='RCUSERS',
        schema='DMITRYMITROFANOV',
    )
    return ctx

def get_visits_detailed(ctx, table_name):
    cs = ctx.cursor()
    try:
        for (order_id) in cs.execute("SELECT distinct order_id FROM vkamala_order2"):
            r = get_data_chunk(API_APPOINTMENT_DETAILED, str(order_id))
            write_to_sf_table(ctx, table_name, json.dumps(r))
    finally:
        cs.close()


def write_to_sf_table(ctx, table_name, data):
    # Gets the version

    cs = ctx.cursor()
    try:
        # cs.execute("insert into "+table_name+" (select PARSE_JSON('%s'))" % data)
        cs.execute(
            "merge into " + table_name + " t using (select parse_json('%s') v) s on s.v = parse_json(t.v) when not matched then insert (t.v) values (s.v)" % data)
    finally:
        cs.close()

def del_from_table(ctx, table_name):
    # Gets the version

    cs = ctx.cursor()
    try:
        # cs.execute("insert into "+table_name+" (select PARSE_JSON('%s'))" % data)
        cs.execute(
            "delete from " + table_name)
    finally:
        cs.close()