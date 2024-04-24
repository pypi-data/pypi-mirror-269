import os
import time as time_module
import traceback
from datetime import datetime, timedelta

from pprint import pprint

import pandas as pd
import digitalarztools.pipelines.weather_data.ncar_rda.rdams_client as rc
from digitalarztools.pipelines.weather_data.ncar_rda.rda_enum import RDAStatus, RDAFormat

current_dir = os.path.dirname(__file__)
docs_dir = os.path.join(current_dir, 'docs')


class GlobalForecast:
    """
        Research Data Archive (RDA) apps clients utils
        datasets details https://rda.ucar.edu/datasets/
        for token generation https://rda.ucar.edu/accounts/profile/
        documentation https://github.com/NCAR/rda-apps-clients/blob/main/docs/README.md

        ds084.1 - NCEP GFS 0.25 Degree Global Forecast Grids Historical Archive
        data access https://rda.ucar.edu/datasets/ds084.1/dataaccess/
        pip install rda-apps-clients

        sample control file
              {'dataset': 'ds084.1',
                 'date': '202404200600/to/202405060600',
                 'datetype': 'valid',
                 'elon': 79.29198455810547,
                 'level': 'HTGL:2',
                 'nlat': 37.089423898000064,
                 'oformat': 'grib',
                 'param': 'R H',
                 'product': '384-hour Forecast',
                 'slat': 23.694683075000057,
                 'wlon': 60.87859740400006}
    """

    def __init__(self, is_meta_data_req=False):
        self.ds = "ds084.1"
        self.metadata_df = self.get_metadata() if is_meta_data_req else pd.DataFrame()

    def get_summary(self):
        res = rc.get_summary(self.ds)
        pprint(res)

    def get_metadata(self) -> pd.DataFrame:
        res = rc.get_metadata(self.ds)
        df = pd.DataFrame(res['data']['data'])
        return df

    def save_metadata(self):
        fp = os.path.join(os.path.dirname(__file__), "ds084.1_meta_data.xlsx")
        # print(fp)
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        self.metadata_df.to_excel(fp)

    def get_common_product(self, params_of_interest: list):
        # Define the parameters of interest
        # params_of_interest = ["T MAX", "T MIN", "TMP", "R H", "A PCP"]

        # Filter the DataFrame to only include rows with these parameters
        filtered_df = self.metadata_df[self.metadata_df['param'].isin(params_of_interest)]

        # Group by 'product' and collect unique parameters associated with each product
        grouped_products = filtered_df.groupby('product')['param'].unique()
        grouped_products_df = pd.DataFrame(grouped_products).reset_index()
        # Filter to find products associated with all specified parameters
        # common_products = grouped_products[grouped_products.apply(lambda x: set(params_of_interest).issubset(set(x)))]

        # Display the common products
        # print(common_products)
        # return common_products['product'].values.tolist()
        return grouped_products_df

    def get_distinct_product_params(self, product) -> dict:
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        product_df = self.metadata_df[self.metadata_df['product'].str.contains(product, na=False)]
        product_df = product_df.drop_duplicates(subset='param')
        params = dict(zip(product_df['param'], product_df['param_description']))
        return params

    def get_distinct_param_name_list(self) -> dict:
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        # params = self.metadata_df.param.unique().tolist()
        params_df = self.metadata_df.drop_duplicates(subset='param')
        params = dict(zip(params_df['param'], params_df['param_description']))
        # pprint(params)
        return params

    def get_distinct_param_product_list(self, param_name: list) -> list:
        param_df = self.get_params_metadata(param_name)
        products = param_df['product'].unique().tolist()
        # pprint(products)
        return products

    def get_params_metadata(self, param_names: list, save_file=False) -> pd.DataFrame:
        # param_df = self.metadata_df[self.metadata_df.param_description.str.contains("temperature", case=False)]
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        param_df = self.metadata_df[self.metadata_df.param.isin(param_names)]
        if save_file:
            fp = os.path.join(os.path.dirname(__file__), f"ds084.1_{'_'.join(param_names)}.xlsx")
            param_df.to_excel(fp)
        # pprint(param_df.shape)
        # pprint(param_df)
        return param_df

    def get_param_product_metadata(self, param_names: list, product) -> pd.DataFrame:
        param_df = self.get_params_metadata(param_names)
        product_df = param_df[param_df['product'].str.contains(product)]
        return product_df

    def get_latest_request_dates(self, product_df: pd.DataFrame,time_delta_hrs=-384, delta_in_days=0) -> str:
        start, end = self.get_product_available_dates(product_df)
        end_date = end + timedelta(days=delta_in_days) if delta_in_days <= 0 else end
        # as product is 6-hour Minimum (initial+378 to initial+384)
        start_date = end_date + timedelta(hours=time_delta_hrs)
        start_date_time_string = start_date.strftime("%Y%m%d%H%M")
        end_date_time_string = end_date.strftime("%Y%m%d%H%M")
        return f"{start_date_time_string}/to/{end_date_time_string}"

    def get_product_available_dates(self, product_df: pd.DataFrame):
        date_format = "%Y%m%d%H%M"
        start_date = datetime.strptime(str(product_df['start_date'].min()), date_format)
        end_date = datetime.strptime(str(product_df['end_date'].max()), date_format)
        return start_date, end_date

    def get_product_levels_info(self, product_df: pd.DataFrame, level_name='HTGL'):
        for levels in product_df.levels:
            level_df = pd.DataFrame(levels)
            gb = level_df.groupby('level')
            for level, group_df in gb:
                # info = f'{level}:' + '/'.join(ISBL_levels)
                if level == level_name:
                    info = f'{level}:' + '/'.join(group_df['level_value'].values.tolist())
                    return info

    def save_control_files_template(self):
        fp = os.path.join(docs_dir, "ds084.1_general_template.txt")
        rc.write_control_file_template(self.ds, fp)
        print("Saved control file template to {}".format(fp))

    def get_request_params(self):
        control_file_name = os.path.join(docs_dir, f"{self.ds}_t_max_template.txt")
        _dict = rc.read_control_file(control_file_name)
        return _dict

    def submit_control_files(self, format: RDAFormat = RDAFormat.grib, bbox: list = [], request_params: dict = None):
        if request_params is None:
            request_params = self.get_request_params()
            param_product_df = self.get_param_product_metadata(request_params['param'], request_params["product"])
            if not param_product_df.empty:
                request_params['level'] = self.get_product_levels_info(param_product_df)
                request_params['date'] = self.get_latest_request_dates(param_product_df)
        if format.value == "csv":
            request_params['oformat'] = 'csv'
        else:
            request_params['oformat'] = format.value if format.value else 'grib'
        if len(bbox) >= 4:
            request_params['slat'] = bbox[1]
            request_params['nlat'] = bbox[3]
            request_params['wlon'] = bbox[0]
            request_params['elon'] = bbox[2]
        pprint(request_params)
        # if len(params) > 0:
        #     request_params['param'] = "/".join(params)

        # res_fp = os.path.join(os.path.dirname(__file__), f"response_{_dict['date'].replace('/','_')}.json")
        res = rc.submit_json(request_params)
        pprint(res)
        # with open(res_fp, 'w') as f:
        #     f.write(json.dumps(res))
        req_id = res['data']['request_id']
        return req_id, request_params

    @staticmethod
    def check_ready(request_idx: str, wait_interval=120):
        """
        https://github.com/NCAR/rda-apps-clients/blob/main/src/python/request_workflow_example.ipynb
        """
        request_status = None
        """Checks if a request is ready."""
        for i in range(10):  # 100 is arbitrary. This would wait 200 minutes for request to complete
            res = rc.get_status(request_idx)
            request_status = res['data']['status']
            if request_status == 'Completed':
                return True, request_status
            print(request_status)
            print('Not yet available. Waiting ' + str(wait_interval) + ' seconds.')
            time_module.sleep(wait_interval)
        return False, request_status

    def download_files(self, request_idx: str, output_dir: str):
        is_ready, status = self.check_ready(request_idx)
        file_name = None
        if is_ready:
            ret = rc.get_filelist(request_idx)
            if len(ret['data']) == 0:
                return ret

            filelist = ret['data']['web_files']

            # token = rc.get_authentication()
            # file_name = rc.download(request_idt_id)
            web_files = set(list(map(lambda x: x['web_path'], filelist)))
            rc.download_files(web_files, output_dir)
        return is_ready, status

    @staticmethod
    def purge_request(request_idx: str) -> RDAStatus:
        try:
            res = rc.purge_request(request_idx)
            pprint(res)
            if res['http_response'] == 421:
                return RDAStatus.Deleted
            elif res['http_response'] == 200:
                return RDAStatus.Purged
        except Exception as e:
            traceback.print_exc()
        return RDAStatus.Error
