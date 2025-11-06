import pandas as pd

from src.pipelines.run_optimization import run_optimization
from src.pipelines.run_postprocess import run_postprocess
from src.pipelines.run_preprocess import run_preprocess


def main() -> None:
    # データの読み込み
    timeseries_df = pd.read_csv("data/demand_sample.csv")
    generator_parameters_df = pd.read_csv("data/generator_parameters_sample.csv")
    # 前処理
    input_data = run_preprocess(timeseries_df, generator_parameters_df)

    # 最適化の実行
    model_output = run_optimization(input_data)

    # 後処理
    structured_output = run_postprocess(model_output)
    print(structured_output)

    # 結果の出力
    pass


if __name__ == "__main__":
    main()
