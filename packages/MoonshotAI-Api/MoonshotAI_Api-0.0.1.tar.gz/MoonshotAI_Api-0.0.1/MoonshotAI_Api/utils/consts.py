QUERY_DATA_URL = 'https://sulbfowah3.execute-api.eu-west-2.amazonaws.com/prod/api/{account_name}/querydata/?job=inference&kpi={' \
                 'kpi}&predtime={pred_time}&startdate={start_date}&enddate={end_date}&datetype={date_type}'

GET_DATA_URL = 'https://sulbfowah3.execute-api.eu-west-2.amazonaws.com/prod/api/{account_name}/getdata/?queryid={query_id}'
GET_STATUS_URL = 'https://sulbfowah3.execute-api.eu-west-2.amazonaws.com/prod/api/{account_name}/getdata/?queryid={query_id}&job={job}'

DEFAULT = 'default'
QUERY_ID = 'query_id'
URL = 'URL'
SUCCESS = 'SUCCEEDED'
FAILED = 'FAILED'
RUNNING = 'RUNNING'
IS_READY = 'isready'
MAX_RETRIES = 15
CSV_FILE = 'data_file.csv'
CHUNK_SIZE = 2 ** 14  # 16KB, Chunk size for iterating over the stream
