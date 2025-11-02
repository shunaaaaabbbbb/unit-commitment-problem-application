# 🔥 Unit Commitment Problem Solver (Basic Edition)

This project optimizes the **operation schedule of multiple generators** to meet daily power demand while minimizing total cost.  
It implements the **basic Unit Commitment Problem (UCP)** using [PuLP](https://coin-or.github.io/pulp/) and outputs both numerical results and visualizations.

> 💡 日本語補足  
> 発電機の起動・停止スケジュールを最適化する数理最適化アプリケーションです。  
> 需要を満たしつつ、稼働コスト・起動コスト・停止コストの合計を最小化します。

---

## 🧩 Features

- Mathematical optimization for the **basic UCP formulation**
- Input data handled as simple CSVs
- Minimizes total cost = running + startup + shutdown
- Clean modular design (I/O, preprocessing, modeling, visualization)
- Ready for future extensions (constraints, UI, emissions, etc.)

---

## 🧱 Directory Structure

```
unit-commitment-problem-application/
├── data/
│ ├── demand.csv # Daily power demand
│ └── furnace_params.csv # Generator parameters
│
├── models/
│ └── ucp_basic.py # PuLP-based mathematical model
│
├── pipelines/
│ └── run_ucp_pipeline.py # End-to-end execution pipeline
│
├── utils/
│ ├── io_handler.py # Data I/O
│ ├── preprocess.py # Data preparation
│ ├── postprocess.py # Output processing
│ └── visualize.py # Visualization functions
│
├── output/
│ ├── schedule.csv # Optimal schedule (per generator/day)
│ ├── summary.csv # Summary of cost and utilization
│ └── charts/
│ ├── output_vs_demand.png # Output vs. demand line chart
│ └── cost_trend.png # Daily cost trend
│
├── app.py # Entry point (CLI)
├── requirements.txt # Dependencies
└── LICENSE # MIT License

```
