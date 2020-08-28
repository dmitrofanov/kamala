from cx import *
from sf import *
import logging
import uuid
import os
import glob

logging.basicConfig(
    # force=True,
    # filename='test.log',
    # filemode='w',
    format='%(asctime)s - %(message)s',
    # level=logging.INFO
    level=logging.INFO
)

this_run = uuid.uuid1()


def save_chunk(data, name):
    with open(os.path.join(base_path, 'chunks', f'{name}.json',), 'w') as f:
        f.write(data)


def cleanup_chunk_dir():
    logging.info('Cleaning up the /chunks/ dir')
    files = glob.glob(os.path.join(base_path, 'chunks\\*'))
    for f in files:
        logging.info(f'File {f} removed')
        os.remove(f)


def create_chunks_gitkeep():
    logging.info('Creating .gitkeep file in /chunks/ dir')
    f = open(os.path.join(base_path, 'chunks\\.gitkeep'), 'w')
    f.close()


def push_api_chunks(cs, api_name, continue_expr):
    cleanup_chunk_dir()
    # delete_from_table(cs, api_name)
    drop_table(cs, api_name)
    create_table(cs, api_name)
    chunks = get_chunks(api_name, continue_expr)
    for chunk, name in chunks:
        logging.info(f'Saving chunk locally: {name}')
        save_chunk(chunk, name)
    load_to_table(cs, api_name, this_run)
    cleanup_chunk_dir()


def push_clt_data(cs):
    def continue_expr(j):
        result = j['count'] > 0
        logging.info(
            f"push_clt_data continue_expr -- count: {j['count']}, continue? {result}")
        return result
    push_api_chunks(cs, API_CLT_NAME, continue_expr)


def push_acl_data(cs):
    def continue_expr(j):
        result = j['offset'] < j['total_count']
        logging.info(
            f"push_acl_data continue_expr -- offset: {j['offset']}, total_count: {j['total_count']}, continue? {result}")
        return result
    push_api_chunks(cs, API_ACL_NAME, continue_expr)


def push_usr_data(cs):
    def continue_expr(j):
        result = j['count'] > 0
        logging.info(
            f"push_usr_data continue_expr -- count: {j['count']}, continue? {result}")
        return result
    push_api_chunks(cs, API_USR_NAME, continue_expr)


def push_svc_data(cs):
    def continue_expr(j):
        result = j['offset'] == 40000
        logging.info(
            f"push_svc_data continue_expr -- offset: {j['offset']}, continue? {result}")
        return result
    push_api_chunks(cs, API_SVC_NAME, continue_expr)


def push_all():
    ctx = connect()
    cs = ctx.cursor()

    push_acl_data(cs)
    push_clt_data(cs)
    push_usr_data(cs)
    push_svc_data(cs)
