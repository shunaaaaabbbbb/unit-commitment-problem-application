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


def preprocess_generator_parameters(input_data: pd.DataFrame) -> GeneratorParameters:
    return GeneratorParameters(
        generator_id=str(input_data["generator_id"].iloc[0]),
        pmin=float(input_data["Pmin"].iloc[0]),
        pmax=float(input_data["Pmax"].iloc[0]),
        cost_run=float(input_data["cost_run"].iloc[0]),
        cost_start=float(input_data["cost_start"].iloc[0]),
        cost_stop=float(input_data["cost_stop"].iloc[0]),
    )
