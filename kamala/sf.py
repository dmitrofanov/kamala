import snowflake.connector
import json
import logging


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


def get_table_name(api_name, prefix="KAMALA_"):
    return prefix + api_name


def create_table(cs, api_name):
    l_sql = f"create table {get_table_name(api_name)} (v variant, inserted_at timestamp_ntz, etl_id VARCHAR(50))"
    cs.execute(l_sql)


def drop_table(cs, api_name):
    l_sql = f"drop table if exists {get_table_name(api_name)}"
    cs.execute(l_sql)


def merge_to_table(cs, api_name, data, etl_id):
    l_sql = "merge into {} t using (select parse_json('{}') v, current_timestamp ts, '{}' etl_id) s \
             on s.v = parse_json(t.v) when not matched then insert (t.v, t.inserted_at, t.etl_id) values (s.v, s.ts, s.etl_id)"
    #l_sql = l_sql.format(get_table_name(api_name), data.replace("'", r"\u0027"), etl_id)
    l_sql = l_sql.format(get_table_name(api_name), data, etl_id)
    logging.debug(l_sql)
    cs.execute(l_sql)


def delele_from_table(cs, api_name):
    l_sql = "delete from {}"
    l_sql = l_sql.format(get_table_name(api_name))
    cs.execute(l_sql)
