import snowflake.connector
import json
import logging
import subprocess
import os
base_path = os.getcwd()


def connect():
    # Opens a connection
    ctx = snowflake.connector.connect(
        user='dmitry.mitrofanov',
        password='o22Dm1trof@nova',
        account='ringcentral',
        authenticator='https://ringcentral.okta.com/',
        warehouse='RCUSERS_WH',
        database='RCUSERS',
        schema='DMITRYMITROFANOV',
    )
    return ctx


def get_table_name(api_name, prefix="KAMALA_"):
    return prefix + api_name


def create_table(cs, api_name):
    l_sql = f"create table {get_table_name(api_name)} (v variant, inserted_at timestamp_ntz, etl_id VARCHAR(50), filename VARCHAR(50))"
    cs.execute(l_sql)


def drop_table(cs, api_name):
    table_name = get_table_name(api_name)
    logging.info(f'Dropping table {table_name}')
    l_sql = f'drop table if exists {table_name}'
    cs.execute(l_sql)


def merge_to_table(cs, api_name, data, etl_id):
    table_name = get_table_name(api_name)
    logging.info(f'Merging to table {table_name}')
    l_sql = "merge into {table_name} t using (select parse_json('{data}') v, current_timestamp ts, '{etl_id}' etl_id) s \
             on s.v = parse_json(t.v) when not matched then insert (t.v, t.inserted_at, t.etl_id) values (s.v, s.ts, s.etl_id)"
    cs.execute(l_sql)


def delete_from_table(cs, api_name):
    table_name = get_table_name(api_name)
    logging.info(f'Deleting from table {table_name}')
    l_sql = f'delete from {table_name}'
    cs.execute(l_sql)


def execute_command(command):
    logging.info(f'Executing command: {command}')
    subprocess.run(command, shell=True, check=True)


def load_to_table(cs, api_name, etl_id):
    path_to_data = os.path.join(base_path, 'chunks')

    table_name = get_table_name(api_name)

    logging.info(f'Loading data for table {table_name}')

    command = r'create or replace temporary stage cx_api_stage file_format = cx_api_format;'
    logging.info(command)
    cs.execute(command)

    command = f"PUT file:///{path_to_data}\\* @cx_api_stage;"
    logging.info(command)
    cs.execute(command)

    command = f'''copy into {table_name}(v, inserted_at, etl_id, filename)
from (select $1, current_timestamp(), '{etl_id}', metadata$filename
      from @cx_api_stage/ t)
on_error = 'ABORT_STATEMENT';'''
    logging.info(command)
    cs.execute(command)
