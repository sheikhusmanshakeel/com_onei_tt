import logging
import pandas as pd
import yaml
import sys

from carbon_footprint.cov_calculator import COVCalculator

logger = logging.getLogger('cov')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    try :
        f = open("config.yml")
        values = yaml.load(f)
        cov_calc = COVCalculator(values["from_date"], values["to_date"], values["api_url"], values["variable"],
                                 values["asset_id"], values["output_file_location"],
                                 pd.read_csv(values["power_measurement_file"]))
        cov_calc.process()
    except:
        logger.critical("Exiting cov calculation", exc_info=True)
        sys.exit(1)
