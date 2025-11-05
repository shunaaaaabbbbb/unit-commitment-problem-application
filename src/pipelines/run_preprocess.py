import pandas as pd

from src.logic.preprocess import (
    preprocess_generator_parameters,
    preprocess_timeseries_data,
)
from src.schemas.data_schema import InputData


def run_preprocess(
    timeseries_df: pd.DataFrame, generator_parameters_df: pd.DataFrame
) -> InputData:
    return InputData(
        timeseries=preprocess_timeseries_data(timeseries_df),
        parameters=preprocess_generator_parameters(generator_parameters_df),
    )
