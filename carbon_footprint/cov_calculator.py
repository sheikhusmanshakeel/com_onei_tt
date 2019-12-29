import logging
import pandas as pd
import requests
from pandas.io.json import json_normalize
from datetime import  datetime
logger = logging.getLogger("cov")


class COVCalculator:
    """
    This class fetches data from two sources and then calculate Change of Value for the entire time-series
    """

    def __init__(self, from_date, to_date, api_url, variable, asset_id, output_file_location, df):
        self.from_date = from_date
        self.to_date = to_date
        self.df_pm_raw = df
        self.api_url = api_url
        self.variable = variable
        self.asset_id = asset_id
        self.output_file_location = output_file_location

        local_vars = locals()
        local_vars.pop("df")
        local_vars.pop("self")
        for k, v in local_vars.items():
            logger.debug("\t{0}: {1}".format(k, v))

    def process_pm_file(self):
        """
        Processes the power management data into 30 minute intervals
        :return:
        """
        self.df_pm_raw["Time"] = pd.to_datetime(self.df_pm_raw["Time"])
        #  Filter out the variable and asset id since we are only interested in the ones provided in the config file
        df_slice = (self.df_pm_raw[
            (self.df_pm_raw["Variable"] == self.variable) & (self.df_pm_raw["AssetId"] == self.asset_id)]).copy()
        df_slice.drop(["Variable", "AssetId"], axis=1, inplace=True)
        df_slice = df_slice.resample("30min", on="Time").sum()
        df_slice["Variable"] = self.variable
        df_slice["AssetId"] = self.asset_id
        return df_slice

    def get_ci_data_from_api(self):
        """
        Makes Api call to fetch data
        :return:
        """
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(self.api_url, headers=headers)
        logger.info("Api response: {0}".format(response.status_code))
        if not response.ok:
            logger.critical("Api did not return valid response")
            raise Exception("Invalid response returned from Api call")
        data = response.json()["data"]
        df_api = json_normalize(data)
        return df_api

    def process_carbon_intensity(self):
        """
        Makes API call to get carbon intensity data and return the dataframe after changing column names and date format
        :return:
        """
        df_api = self.get_ci_data_from_api()
        df_api.rename(
            columns={"intensity.forecast": "forecast", "intensity.actual": "actual", "intensity.index": "index"},
            inplace=True)
        df_api["to"] = pd.to_datetime(df_api["to"])
        df_api["from"] = pd.to_datetime(df_api["from"])
        df_api["Time"] = df_api["to"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df_api["Time"] = pd.to_datetime(df_api["Time"])
        return df_api

    def process(self):
        """
        Main function to drive cov calculation
        :return:
        """
        logger.info("COV process started")
        self.from_date = datetime.strptime(str(self.from_date), '%Y%m%d').strftime('%Y-%m-%d')
        self.to_date = datetime.strptime(str(self.to_date), '%Y%m%d').strftime('%Y-%m-%d')
        self.api_url = self.api_url.format(self.from_date, self.to_date)
        df_pm = self.process_pm_file()
        df_api = self.process_carbon_intensity()
        merged_df = pd.merge(df_pm, df_api, on=["Time"], how="inner")
        merged_df.insert(0, "HalfHourId", range(1, len(merged_df) + 1))
        merged_df.to_csv(self.output_file_location, index=False)
        logger.info("File saved at: {0}".format(self.output_file_location))
        logger.info("COV process finished")
