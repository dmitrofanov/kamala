import snowflake.connector
import json
import requests


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


def mrg_to_table(ctx, table_name, data):
    # Merge data to table

    l_sql = "merge into {} t using (select parse_json('{}') v) s on s.v = parse_json(t.v) when not matched then insert (t.v) values (s.v)"
    #l_sql = l_sql.format(table_name, json.dumps(data).replace("'", ""))
    l_sql = l_sql.format(table_name, json.dumps(data))
    cs = ctx.cursor()
    try:
        cs.execute(l_sql)
    finally:
        cs.close()


def del_from_table(ctx, table_name):
    # Delete data from table

    cs = ctx.cursor()
    try:
        cs.execute(
            "delete from " + table_name)
    finally:
        cs.close()