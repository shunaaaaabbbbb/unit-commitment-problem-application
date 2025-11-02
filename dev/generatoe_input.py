# dev/generate_sample_data.py
import os
from datetime import date

import numpy as np
import pandas as pd


def generate_demand_data(
    start_date: date, end_date: date, seed: int = 42
) -> pd.DataFrame:
    """1年分の電力需要データを日次で生成（再現性あり）"""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # 需要は300〜500MWの範囲で季節的に揺らぐサイン波 + ノイズ
    base_demand = 400 + 80 * np.sin(np.linspace(0, 2 * np.pi, len(dates)))
    noise = rng.normal(0, 20, len(dates))
    demand = np.clip(base_demand + noise, 250, 550)

    df = pd.DataFrame({"date": dates.date, "demand": demand.round(1)})
    return df


def generate_generator_parameters(num_generators: int, seed: int = 42) -> pd.DataFrame:
    """発電機のパラメータをランダム生成（再現性あり）"""
    rng = np.random.default_rng(seed)
    ids = [f"G{i+1}" for i in range(num_generators)]
    pmin = rng.integers(30, 150, num_generators)
    pmax = pmin + rng.integers(100, 250, num_generators)
    cost_run = rng.uniform(3.0, 6.0, num_generators).round(2)
    cost_start = rng.integers(80, 200, num_generators)
    cost_stop = rng.integers(40, 120, num_generators)

    return pd.DataFrame(
        {
            "generator_id": ids,
            "Pmin": pmin,
            "Pmax": pmax,
            "cost_run": cost_run,
            "cost_start": cost_start,
            "cost_stop": cost_stop,
        }
    )


def main(num_generators: int = 3, output_dir: str = "data", seed: int = 42) -> None:
    """データ生成のメイン関数"""
    os.makedirs(output_dir, exist_ok=True)

    start_date = date(2024, 4, 1)
    end_date = date(2025, 3, 31)

    demand_df = generate_demand_data(start_date, end_date, seed)
    gen_df = generate_generator_parameters(num_generators, seed)

    demand_df.to_csv(os.path.join(output_dir, "demand.csv"), index=False)
    gen_df.to_csv(os.path.join(output_dir, "generator_parameters.csv"), index=False)

    print(f"✅ Generated {len(demand_df)} days of demand data.")
    print(f"✅ Generated parameters for {num_generators} generators.")
    print(f"📁 Files saved in '{output_dir}/'")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate sample demand and generator data."
    )
    parser.add_argument(
        "--num-generators", type=int, default=3, help="Number of generators"
    )
    parser.add_argument(
        "--output-dir", type=str, default="data", help="Output directory"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    main(num_generators=args.num_generators, output_dir=args.output_dir, seed=args.seed)
