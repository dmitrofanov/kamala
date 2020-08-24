from cx import *
from sf import *
import logging
import uuid

logging.basicConfig(
    force=True,
    filename='test.log',
    filemode='w',
    format='%(asctime)s - %(message)s',
    # level=logging.INFO
    level=logging.DEBUG
)

this_run = uuid.uuid1()


def push_data_acl():
    ctx = connect()
    cs = ctx.cursor()
    drop_table(cs, API_ACL_NAME)
    create_table(cs, API_ACL_NAME)
    logging.info(f'Table for {API_ACL_NAME} has been recreated')

    offset = 0
    chunk = get_data_chunk(API_ACL_NAME, offset)
    parsed_chunk = json.loads(chunk)
    total_count = int(parsed_chunk["total_count"])
    while offset < total_count:
        chunk = get_data_chunk(API_ACL_NAME, offset)
        merge_to_table(cs, API_ACL_NAME, chunk, this_run)
        offset = offset + 50


def push_data_usr():
    ctx = connect()
    cs = ctx.cursor()
    drop_table(cs, API_USR_NAME)
    create_table(cs, API_USR_NAME)
    logging.info(f'Table for {API_USR_NAME} has been recreated')

    offset = 0
    has_more_pages = True
    while has_more_pages:
        chunk = get_data_chunk(API_USR_NAME, offset)
        parsed_chunk = json.loads(chunk)

        has_more_pages = False if parsed_chunk['count'] < 50 else True

        merge_to_table(cs, API_USR_NAME, json.dumps(parsed_chunk), this_run)
        offset = offset + 50


def push_data_clt():
    ctx = connect()
    cs = ctx.cursor()
    drop_table(cs, API_CLT_NAME)
    create_table(cs, API_CLT_NAME)
    logging.info(f'Table for {API_CLT_NAME} has been recreated')

    offset = 0
    has_more_pages = True
    while has_more_pages:
        chunk = get_data_chunk(API_CLT_NAME, offset)
        parsed_chunk = json.loads(chunk)

        # parsed_chunk.pop('json_data', None)
        for i in parsed_chunk["items"]:
            i.pop('json_data', None)
            i.pop('multi_image', None)
            i.pop('multi_file', None)
            pass
        has_more_pages = False if parsed_chunk['count'] < 50 else True

        merge_to_table(cs, API_CLT_NAME, chunk, this_run)
        # merge_to_table(cs, API_CLT_NAME, chunk, this_run)
        offset = offset + 50
