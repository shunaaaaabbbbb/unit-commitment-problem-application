from datetime import datetime

import pandas as pd

from src.schemas.data_schema import GeneratorParameters, InputTimeSeriesData


def preprocess_timeseries_data(input_data: pd.DataFrame) -> list[InputTimeSeriesData]:
    data = []
    for i, (_, row) in enumerate(input_data.iterrows()):
        date = datetime.strptime(row["date"], "%Y-%m-%d")
        demand = float(row["demand"])
        data.append(InputTimeSeriesData(date=date, date_index=i + 1, demand=demand))
    return data


def preprocess_generator_parameters(
    input_data: pd.DataFrame,
) -> list[GeneratorParameters]:
    parameters_list = []
    for _, (_, row) in enumerate(input_data.iterrows()):
        generator_id = str(row["generator_id"])
        pmin = float(row["Pmin"])
        pmax = float(row["Pmax"])
        cost_run = float(row["cost_run"])
        cost_start = float(row["cost_start"])
        cost_stop = float(row["cost_stop"])
        min_operation_time = int(row["min_operation_time"])
        max_operation_time = int(row["max_operation_time"])
        generator_parameters = GeneratorParameters(
            generator_id=generator_id,
            pmin=pmin,
            pmax=pmax,
            cost_run=cost_run,
            cost_start=cost_start,
            cost_stop=cost_stop,
            min_operation_time=min_operation_time,
            max_operation_time=max_operation_time,
        )
        parameters_list.append(generator_parameters)
    return parameters_list
