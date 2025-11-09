import os
from datetime import datetime

import pandas as pd

from src.pipelines.create_output import create_output
from src.pipelines.run_optimization import run_optimization
from src.pipelines.run_postprocess import run_postprocess
from src.pipelines.run_preprocess import run_preprocess


def main() -> None:
    today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = f"output/{today}"
    os.makedirs(output_dir, exist_ok=True)

    # データの読み込み
    timeseries_df = pd.read_csv("data/demand_sample.csv")
    generator_parameters_df = pd.read_csv("data/generator_parameters_sample.csv")
    # 前処理
    input_data = run_preprocess(timeseries_df, generator_parameters_df)

    # 最適化の実行
    model_output = run_optimization(input_data, output_dir)

    # 後処理
    overall_output = run_postprocess(model_output, input_data)

    # 結果の出力
    create_output(overall_output, output_dir)


if __name__ == "__main__":
    main()
