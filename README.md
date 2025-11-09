# Power Plant Scheduling Optimization Model
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![PuLP](https://img.shields.io/badge/PuLP-MILP%20modeler-orange)
![uv](https://img.shields.io/badge/env-uv%20managed-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)
![Optimization](https://img.shields.io/badge/topic-Unit%20Commitment%20Problem-blue)

*(日本語verは下にあります / See below for Japanese)*
## Overview
This application solves a simplified **Unit Commitment Problem (UCP)** to generate optimal operation schedules for multiple power plants.
It reads demand and generator parameter data from CSV files, structures them with **Pydantic**, formulates and solves a **Mixed Integer Linear Programming (MILP)** model using **PuLP**, and provides a complete pipeline from preprocessing to visualization of the results.

## Tech Stack
- Python (3.10+)
- PuLP (optimization modeling & solver)
- Pandas / NumPy (data processing)
- Matplotlib / Plotly (visualization)
- Pydantic v2 (data schema management)
- uv (environment setup & dependency management)

## How to Run
1. Clone the repository.
2. Install dependencies using **uv**:
   ```bash
   uv sync
3. Run the main script:
    ```bash
    uv run python app.py
    ```
    The results will be saved in the `output/<timestamp>/` directory.

## Directory Structure
```
unit-commitment-problem-application/
├── app.py
├── data/
│   ├── demand_sample.csv
│   └── generator_parameters_sample.csv
├── output/
│   └── <timestamp>/
│       ├── demand_vs_generation.png
│       └── solver.log
├── src/
│   ├── logic/
│   │   ├── postprocess.py
│   │   ├── preprocess.py
│   │   └── visualize.py
│   ├── models/
│   │   └── solver.py
│   ├── pipelines/
│   │   ├── create_output.py
│   │   ├── run_optimization.py
│   │   ├── run_postprocess.py
│   │   └── run_preprocess.py
│   ├── schemas/
│   │   └── data_schema.py
│   └── utils/
│       └── safe_cast.py
├── pyproject.toml
└── README.md
```

---

# 発電スケジューリング最適化モデル

## 概要
本アプリケーションは、単純化した起動停止問題（Unit Commitment Problem）を解くことで、複数発電機の最適運用スケジュールを生成する。需要や設備パラメータのCSVを読み込み、Pydanticで構造化し、PuLPで混合整数最適化モデルを構築して解き、結果を可視化する処理まで一貫して行う。

## 使用技術
- Python (3.10以上)
- PuLP（最適化モデリング & ソルバー）
- Pandas / NumPy（データ処理）
- Matplotlib / Plotly（静的可視化）
- Pydantic v2（データスキーマ管理）
- uv（環境構築・依存関係管理）

## 実行方法
1. リポジトリのクローン
2. uvを用いた依存関係のインストール
   ```bash
   uv sync
   ```
3. スクリプトの実行
   ```bash
   uv run python app.py
   ```
   結果は `output/<timestamp>/` に保存

## ディレクトリ構成
```
unit-commitment-problem-application/
├── app.py
├── data/
│   ├── demand_sample.csv
│   └── generator_parameters_sample.csv
├── output/
│   └── <timestamp>/
│       ├── demand_vs_generation.png
│       └── solver.log
├── src/
│   ├── logic/
│   │   ├── postprocess.py
│   │   ├── preprocess.py
│   │   └── visualize.py
│   ├── models/
│   │   └── solver.py
│   ├── pipelines/
│   │   ├── create_output.py
│   │   ├── run_optimization.py
│   │   ├── run_postprocess.py
│   │   └── run_preprocess.py
│   ├── schemas/
│   │   └── data_schema.py
│   └── utils/
│       └── safe_cast.py
├── pyproject.toml
└── README.md
```
