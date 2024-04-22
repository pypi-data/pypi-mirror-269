import json
import pandas as pd
import urllib3

from marcuslion.apiUtils import get_filename_from_api
import marcuslion.config as config


class RestController:
    """
    MarcusLion RestController class
    """
    _http = urllib3.PoolManager()

    def __init__(self, url_path):
        self._url_path = url_path
        pass

    def _get_url(self, action) -> str:

        print(config.get_config())

        full_url = config.get_base_url() + '/' + config.get_api_version()  + '/' + self._url_path
        if not action is None:
            full_url += '/' + action

        full_url = full_url.replace('//', '/').replace(':/', '://')
        return full_url

    def _get_request(self, action, params, method="GET", preload_content=True, **kwargs):
        full_url = self._get_url(action)

        print(f"_get_request {full_url} {params}")

        resp = self._http.request(method, full_url,
                                  headers={'X-MARCUSLION-API-KEY': config.get_api_key()},
                                  fields=params,
                                  preload_content=preload_content,
                                  **kwargs)

        if resp.status == 401:
            raise ValueError("401: Unauthorized User. URL:" + full_url)
        if resp.status != 200:
            raise ValueError("status: " + full_url + " -> " + (
                str(resp.status) + (" data: " + resp.data.decode()) if resp.data else ""))
        return resp

    def download_file(self, action, params, output_path=None):
        if output_path is None:
            output_path = "."
        resp = self._get_request(action, params, preload_content=False)
        file_name = f"{output_path}/{get_filename_from_api(resp)}"
        with open(file_name, 'wb') as out_file:
            for chunk in resp.stream(1024):
                out_file.write(chunk)

        return out_file.name

    def verify_get_df(self, action=None, params=None) -> pd.DataFrame:
        response = self.verify_get(action, params)
        return pd.DataFrame.from_records(response)

    def verify_get(self, action=None, params=None) -> any:
        # Sending a GET request and getting back response as HTTPResponse object.
        resp = self._get_request(action, params)

        data_str = resp.data.decode()
        if len(data_str) == 0:
            return None

        return json.loads(data_str)

    def verify_get_data(self, action=None, params=None) -> pd.DataFrame:
        data = self.verify_get(action, params)
        if data is None:
            return pd.DataFrame()
        df = pd.DataFrame(data['data'])
        return df
