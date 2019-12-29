import pandas as pd
import pytest
from mock import patch

from carbon_footprint.cov_calculator import COVCalculator


class Response:
    def __init__(self, data, ok, status_code):
        self.data = data
        self.ok = ok
        self.status_code = status_code

    def json(self):
        return self.data


@patch("carbon_footprint.cov_calculator.requests.get")
def test_get_ci_data_from_api_normalized_data(mock_request_get):
    # Arrange
    data = {"data": {"col1": "val1", "col2": "val2", "col3": {"1": 2, "2": 2}}}
    ok = True
    status_code = 200
    r = Response(data, ok, status_code)
    mock_request_get.return_value = r
    cov_cal = COVCalculator(None, None, None, None, None, None, None)

    # Act
    ret_val = cov_cal.get_ci_data_from_api()

    # Assert
    assert isinstance(ret_val, pd.DataFrame)
    assert list(ret_val.columns.values) == ["col1", "col2", "col3.1", "col3.2"]


@patch("carbon_footprint.cov_calculator.logger")
@patch("carbon_footprint.cov_calculator.requests.get")
def test_get_ci_data_from_api_raises_exception(mock_request_get, mock_logger):
    # Arrange
    ok = False
    status_code = 400
    r = Response(None, ok, status_code)
    mock_request_get.return_value = r

    cov_cal = COVCalculator(None, None, None, None, None, None, None)

    # Act and Assert
    with pytest.raises(Exception,  message="Invalid response returned from Api call"):
        cov_cal.get_ci_data_from_api()

    mock_logger.critical.assert_called_once_with("Api did not return valid response")
    mock_logger.info.assert_called_once_with("Api response: {0}".format(status_code))
