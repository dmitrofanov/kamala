create or replace temporary stage cx_api_stage file_format = cx_api_format;

PUT file://C:\Users\dmitry.mitrofanov\codebase\kamala\kamala\chunk.json @cx_api_stage;

copy into kamala_clt(v, inserted_at, etl_id)
from (select $1, current_timestamp(), '123'
      from @cx_api_stage/chunk.json.gz t)
on_error = 'abort_statement';
