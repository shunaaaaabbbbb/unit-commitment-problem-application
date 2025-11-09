from pulp import (
    PULP_CBC_CMD,
    LpBinary,
    LpContinuous,
    LpMinimize,
    LpProblem,
    LpVariable,
    lpSum,
)

from src.schemas.data_schema import InputData


class Solver:
    def __init__(self, input_data: InputData):
        self.timeseries = input_data.timeseries
        self.generator_parameters = input_data.generator_parameters
        self.num_units = len(self.generator_parameters)
        self.num_timeseries = len(self.timeseries)
        self.min_operation_times = [
            generator.min_operation_time for generator in self.generator_parameters
        ]

        self.min_down_times = [
            generator.min_down_time for generator in self.generator_parameters
        ]
        self.pmins = [generator.pmin for generator in self.generator_parameters]
        self.pmaxs = [generator.pmax for generator in self.generator_parameters]
        self.cost_runs = [generator.cost_run for generator in self.generator_parameters]
        self.cost_starts = [
            generator.cost_start for generator in self.generator_parameters
        ]
        self.cost_stops = [
            generator.cost_stop for generator in self.generator_parameters
        ]
        self.ramp_ups = [generator.ramp_up for generator in self.generator_parameters]
        self.ramp_downs = [
            generator.ramp_down for generator in self.generator_parameters
        ]

    def build_model(self) -> None:
        self.model = LpProblem("UnitCommitmentProblem", LpMinimize)
        self.add_variables()
        self.add_constraints()
        self.add_objective()

    def add_variables(self) -> None:
        self.operation = {
            (t, p): LpVariable(f"operation_{t}_{p}", cat=LpBinary)
            for t in range(self.num_timeseries)
            for p in range(self.num_units)
        }
        self.start = {
            (t, p): LpVariable(f"start_{t}_{p}", cat=LpBinary)
            for t in range(self.num_timeseries)
            for p in range(self.num_units)
        }
        self.stop = {
            (t, p): LpVariable(f"stop_{t}_{p}", cat=LpBinary)
            for t in range(self.num_timeseries)
            for p in range(self.num_units)
        }
        self.output = {
            (t, p): LpVariable(f"output_{t}_{p}", lowBound=0, cat=LpContinuous)
            for t in range(self.num_timeseries)
            for p in range(self.num_units)
        }

    def add_constraints(self) -> None:
        # 起動停止変数の関係を表す制約
        for p in range(self.num_units):
            for t in range(self.num_timeseries):
                self.model += self.start[t, p] <= self.operation[t, p]
        for p in range(self.num_units):
            for t in range(1, self.num_timeseries):
                self.model += (
                    self.start[t, p] - self.stop[t, p]
                    == self.operation[t, p] - self.operation[t - 1, p]
                )

        # 開始したら最低でもα期は連続稼働
        for p in range(self.num_units):
            for t in range(self.min_operation_times[p], self.num_timeseries):
                self.model += (
                    lpSum(
                        self.start[s, p]
                        for s in range(t - self.min_operation_times[p], t)
                    )
                    <= self.operation[t, p]
                )

        # 停止したら最低でもβ期間は連続停止
        for p in range(self.num_units):
            for t in range(self.min_down_times[p], self.num_timeseries):
                self.model += (
                    lpSum(self.stop[s, p] for s in range(t - self.min_down_times[p], t))
                    <= 1 - self.operation[t, p]
                )

        # 発電機の出力制約
        for p in range(self.num_units):
            for t in range(self.num_timeseries):
                self.model += self.pmins[p] * self.operation[t, p] <= self.output[t, p]
                self.model += self.output[t, p] <= self.pmaxs[p] * self.operation[t, p]

        # 各日の需要を満たす制約
        for t in range(self.num_timeseries):
            self.model += (
                lpSum(self.output[t, p] for p in range(self.num_units))
                >= self.timeseries[t].demand
            )

        # 各発電機のランプアップ・ランプダウン制約
        for p in range(self.num_units):
            for t in range(1, self.num_timeseries):
                self.model += (
                    self.output[t, p] - self.output[t - 1, p] <= self.ramp_ups[p]
                )
                self.model += (
                    self.output[t - 1, p] - self.output[t, p] <= self.ramp_downs[p]
                )

    def add_objective(self) -> None:
        # 総コストを最小化
        self.model += lpSum(
            self.cost_runs[p] * self.output[t, p]
            + self.cost_starts[p] * self.start[t, p]
            + self.cost_stops[p] * self.stop[t, p]
            for p in range(self.num_units)
            for t in range(self.num_timeseries)
        )

    def solve(self, output_dir: str) -> LpProblem:
        self.model.solve(PULP_CBC_CMD(msg=False, logPath=f"{output_dir}/solver.log"))
        return self.model
