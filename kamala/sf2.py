import snowflake.connector
import json


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


def get_table_name(table_name, prefix="KAMALA_"):
    return prefix + table_name


def mrg_to_table(cs, table_name, data):
    # Merge data to table
    l_sql = "merge into {} t using (select parse_json('{}') v, current_timestamp ts) s on s.v = parse_json(t.v) when not matched then insert (t.v, changed_at) values (s.v, s.ts)"
    l_sql = l_sql.format(get_table_name(table_name), json.dumps(data))
    cs.execute(l_sql)


def del_from_table(cs, table_name):
    # Delete data from table
    l_sql = "delete from {}"
    l_sql = l_sql.format(get_table_name(table_name))
    cs.execute(l_sql)
