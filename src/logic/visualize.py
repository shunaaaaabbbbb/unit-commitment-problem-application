import os

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.schemas.data_schema import OverallOutput


def visualize_generations(overall_output: OverallOutput, output_dir: str) -> None:
    """
    発電機ごとの発電量をPlotlyで可視化（需要は表示しない）。
    構成:
    - 上: 積み上げ棒グラフ（全発電機）
    - 下: 各発電機の棒グラフ（積み上げと同じ色）
    - すべてのy軸スケールを統一
    出力形式: HTML (縦にグラフを並べる)
    """
    os.makedirs(output_dir, exist_ok=True)

    # === OverallOutput → DataFrame変換 ===
    records: list[dict[str, object]] = []
    for generator_output in overall_output.generator_outputs:
        for schedule in generator_output.schedules:
            records.append(
                {
                    "date": schedule.date,
                    "generator_id": generator_output.generator_id,
                    "output": schedule.output,
                }
            )

    if not records:
        raise ValueError("overall_outputに発電量データが含まれていません。")

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    generation_pivot = (
        df.pivot_table(
            index="date", columns="generator_id", values="output", aggfunc="sum"
        )
        .fillna(0.0)
        .sort_index()
    )

    generator_columns = generation_pivot.columns.tolist()

    # === カラーマップ ===
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    color_map = {
        gid: colors[i % len(colors)] for i, gid in enumerate(generator_columns)
    }

    # === y軸スケールを全グラフで統一 ===
    total_output_each_day = generation_pivot.sum(axis=1)
    unified_ymax = float(total_output_each_day.max()) * 1.05  # 少し余裕を持たせる

    # === サブプロット作成 ===
    fig = make_subplots(
        rows=len(generator_columns) + 1,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=[
            "🔹 全発電機の積み上げ発電量",
            *[f"発電機 {gid} の発電量" for gid in generator_columns],
        ],
    )

    # === (1) 積み上げ棒グラフ ===
    for gid in generator_columns:
        fig.add_trace(
            go.Bar(
                x=generation_pivot.index,
                y=generation_pivot[gid],
                name=f"{gid}",
                marker_color=color_map[gid],
                customdata=generation_pivot[generator_columns].to_numpy(),
                hovertemplate="<b>%{x}</b><br>"
                + "<br>".join(
                    [
                        f"{g}: " + "%{customdata[" + str(i) + "]:.2f} MW"
                        for i, g in enumerate(generator_columns)
                    ]
                )
                + "<br><b>合計: %{y:.2f} MW</b>",
            ),
            row=1,
            col=1,
        )

    fig.update_yaxes(range=[0, unified_ymax], row=1, col=1)

    # === (2) 各発電機の棒グラフ ===
    for i, gid in enumerate(generator_columns, start=2):
        fig.add_trace(
            go.Bar(
                x=generation_pivot.index,
                y=generation_pivot[gid],
                name=f"{gid}",
                marker_color=color_map[gid],
                hovertemplate="日付: %{x}<br>発電量: %{y:.2f} MW<br>発電機: " + gid,
            ),
            row=i,
            col=1,
        )
        # 各行に同じy軸範囲を適用
        fig.update_yaxes(range=[0, unified_ymax], row=i, col=1)

    # === レイアウト調整 ===
    fig.update_layout(
        title="⚡ 発電機別 発電量 可視化ダッシュボード（全グラフ共通スケール）",
        xaxis_title="日付",
        yaxis_title="発電量 (MW)",
        template="plotly_white",
        height=350 * (len(generator_columns) + 1),
        showlegend=True,
        barmode="stack",
        legend=dict(
            orientation="h",
            y=1.02,
            x=0.5,
            xanchor="center",
            yanchor="bottom",
        ),
        hovermode="x unified",
        margin=dict(l=60, r=30, t=80, b=40),
    )

    # === 出力 ===
    output_path = os.path.join(output_dir, "generation_dashboard.html")
    fig.write_html(output_path, include_plotlyjs="cdn")
