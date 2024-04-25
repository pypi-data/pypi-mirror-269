from MoonshotAI_Api.utils.consts import QUERY_DATA_URL, GET_DATA_URL, DEFAULT, QUERY_ID, URL, IS_READY, \
    GET_STATUS_URL, RUNNING, MAX_RETRIES, SUCCESS
from MoonshotAI_Api.utils.utils import download_file
from MoonshotAI_Api.utils.output_enum import OutputFormat
import requests
import json
import time


class LTVClient:
    def __init__(self, profile, token, default=False):
        self.profile = profile
        self._account_name = profile
        self.token = token
        self.default = default

    # Default output format - CSV filename
    def fetch_data(self, kpi, pred_time, start_date, end_date, date_type, output_format=OutputFormat.CSV.value):

        # Querying data
        query_id = self.__query_data(kpi=kpi, pred_time=pred_time, start_date=start_date, end_date=end_date,
                                     date_type=date_type)

        # Add wait mechanic to make sure the data is ready
        status = None
        for idx in range(1, MAX_RETRIES):
            status = self.__check_status(query_id=query_id)
            if status == SUCCESS:
                break
            wait = 10 * idx
            time.sleep(wait)

        if status != SUCCESS:
            raise Exception(f"Error getting data with given query id. Query execution status: {status}")

        # Getting data
        url = self.__get_data(query_id=query_id)

        csv_data = download_file(url=url, output_format=output_format)

        # Returning data as stream / CSV filename depends on the output format
        return csv_data

    def __query_data(self, kpi, pred_time, start_date, end_date, date_type):
        headers = {
            "token": self.token,
            "company": self.profile
        }

        if self.default:
            self._account_name = DEFAULT

        url = QUERY_DATA_URL.format(account_name=self._account_name, kpi=kpi, pred_time=pred_time,
                                    start_date=start_date, end_date=end_date, date_type=date_type)

        response = None
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

        except Exception as e:
            if response is not None:
                msg = None
                if isinstance(response.text, dict):
                    msg = json.loads(response.text).get('Message', None)
                elif isinstance(response.text, str):
                    msg = response.text

                if msg is not None:
                    raise Exception(f"Error with status code: {response.status_code}, {msg}")
                raise Exception(f"Error with status code: {response.status_code}, {response.text}")
            raise Exception(f"Error with request: {e}")

        try:
            data = response.json()
            query_id = data[QUERY_ID]
        except Exception as e:
            raise Exception(f"Error getting query id: {e}")

        return query_id

    def __get_data(self, query_id):
        headers = {
            "token": self.token,
            "company": self.profile
        }
        if self.default:
            self._account_name = DEFAULT

        url = GET_DATA_URL.format(account_name=self._account_name, query_id=query_id)

        response = None
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

        except Exception as e:
            if response is not None:
                msg = None
                if isinstance(response.text, dict):
                    msg = json.loads(response.text).get('Message', None)
                elif isinstance(response.text, str):
                    msg = response.text

                if msg is not None:
                    raise Exception(f"Error with status code: {response.status_code}, {msg}")
                raise Exception(f"Error with status code: {response.status_code}, {response.text}")
            raise Exception(f"Error with request: {e}")

        try:
            data = response.json()
            url = data[URL]
        except Exception as e:
            raise Exception(f"Error getting query id: {e}")

        return url

    def __check_status(self, query_id):
        headers = {
            "token": self.token,
            "company": self.profile
        }
        if self.default:
            self._account_name = DEFAULT

        url = GET_STATUS_URL.format(account_name=self._account_name, query_id=query_id, job=IS_READY)

        response = None
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

        except Exception as e:
            if response is not None:
                msg = json.loads(response.text).get('Message', None)
                status = json.loads(response.text).get('Status', None)
                if status == RUNNING:
                    return status

                if msg is not None:
                    raise Exception(f"Error with status code: {response.status_code}, {msg}")
                raise Exception(f"Error with status code: {response.status_code}, {response.text}")
            raise Exception(f"Error with request: {e}")

        try:
            data = response.json()
            status = data['Status']
        except Exception as e:
            raise Exception(f"Error getting query status: {e}")

        return status

