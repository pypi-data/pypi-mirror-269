from MoonshotAI_Api.utils.output_enum import OutputFormat
from MoonshotAI_Api.utils.consts import CHUNK_SIZE, CSV_FILE
import requests


def download_file(url, output_format, chunk_size=CHUNK_SIZE):
    try:
        response = requests.get(url)
        if response.status_code == 200:

            # Return the filename of the downloaded csv file
            if output_format == OutputFormat.CSV.value:
                with open(CSV_FILE, 'wb') as f:
                    f.write(response.content)
                return CSV_FILE

            # Return the content of the downloaded file as a byte stream (can be divided into chunks if needed)
            if output_format == OutputFormat.STREAM.value:
                if chunk_size is None:
                    return response.iter_content()
                return response.iter_content(chunk_size=CHUNK_SIZE)

        raise Exception(f"Error downloading file. Status code: {response.status_code}")

    except Exception as e:
        raise Exception(f"Error downloading file: {e}")
