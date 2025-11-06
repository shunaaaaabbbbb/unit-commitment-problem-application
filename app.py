import pandas as pd

from src.pipelines.run_preprocess import run_preprocess


def main() -> None:
    # データの読み込み
    timeseries_df = pd.read_csv("data/demand_sample.csv")
    generator_parameters_df = pd.read_csv("data/generator_parameters_sample.csv")
    # 前処理
    input_data = run_preprocess(timeseries_df, generator_parameters_df)
    print(input_data)

    # 最適化の実行
    pass

    # 後処理
    pass

    # 結果の出力
    pass


if __name__ == "__main__":
    main()
