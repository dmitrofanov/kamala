from kamala.cx import *
from kamala.sf import *
import logging

logging.basicConfig(filename='test.log',
	filemode='w',
	format='%(asctime)s - %(message)s',
	level=logging.DEBUG
)


def push_data():
	chunk = get_data_chunk(API_ACL_NAME, 19450)
	ctx = connect()
	cs = ctx.cursor()
	mrg_to_table(cs, API_ACL_NAME, chunk)