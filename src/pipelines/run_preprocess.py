import pandas as pd

from src.logic.preprocess import (
    preprocess_generator_parameters,
    preprocess_timeseries_data,
)
from src.schemas.data_schema import InputData


def run_preprocess(
    timeseries_df: pd.DataFrame, generator_parameters_df: pd.DataFrame
) -> InputData:
    timeseries = preprocess_timeseries_data(timeseries_df)
    generator_parameters = preprocess_generator_parameters(generator_parameters_df)
    input_data = InputData(
        timeseries=timeseries, generator_parameters=generator_parameters
    )
    return input_data
