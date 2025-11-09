from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class InputTimeSeriesData(BaseModel):
    date: datetime = Field(..., description="日付 (YYYY-MM-DD)")
    date_index: int = Field(..., description="日付インデックス")
    demand: float = Field(..., description="電力需要 (MW)")


class GeneratorParameters(BaseModel):
    generator_id: str = Field(..., description="発電機ID")
    pmin: float = Field(..., description="最小出力 (MW)")
    pmax: float = Field(..., description="最大出力 (MW)")
    cost_run: float = Field(..., description="運転コスト (円/MW)")
    cost_start: float = Field(..., description="起動コスト (円/回)")
    cost_stop: float = Field(..., description="停止コスト (円/回)")
    min_operation_time: int = Field(..., description="最低稼働期間 (時間)")
    max_operation_time: int = Field(..., description="最大稼働期間 (時間)")

    @field_validator("pmin")
    @classmethod
    def validate_pmin(cls, v: float) -> float:
        if v < 0:
            raise ValueError("最小出力は0以上である必要があります")
        return v

    @field_validator("pmax")
    @classmethod
    def validate_pmax(cls, v: float) -> float:
        if v < 0:
            raise ValueError("最大出力は0以上である必要があります")
        return v

    @field_validator("cost_run")
    @classmethod
    def validate_cost_run(cls, v: float) -> float:
        if v < 0:
            raise ValueError("運転コストは0以上である必要があります")
        return v

    @field_validator("cost_start")
    @classmethod
    def validate_cost_start(cls, v: float) -> float:
        if v < 0:
            raise ValueError("起動コストは0以上である必要があります")
        return v

    @field_validator("cost_stop")
    @classmethod
    def validate_cost_stop(cls, v: float) -> float:
        if v < 0:
            raise ValueError("停止コストは0以上である必要があります")
        return v


class InputData(BaseModel):
    timeseries: list[InputTimeSeriesData] = Field(..., description="電力需要データ")
    generator_parameters: list[GeneratorParameters] = Field(
        ..., description="発電機パラメータ"
    )


class DailySchedule(BaseModel):
    date: datetime = Field(..., description="日付 (YYYY-MM-DD)")
    start: int = Field(..., description="起動状態 (0: 停止, 1: 起動)")
    stop: int = Field(..., description="停止状態 (0: 停止, 1: 停止)")
    operation: int = Field(..., description="稼働状態 (0: 停止, 1: 稼働)")
    output: float = Field(..., description="出力 (MW)")
    cost: float = Field(..., description="コスト (円)")


class GeneratorOutput(BaseModel):
    generator_id: str = Field(..., description="発電機ID")
    schedules: list[DailySchedule] = Field(..., description="日次スケジュール")
    generator_cost: float = Field(..., description="発電機のコスト (円)")
    generator_output: float = Field(..., description="発電機の出力 (MW)")
    generator_operation_days: int = Field(
        ..., description="発電機の稼働状態 (0: 停止, 1: 稼働)"
    )
    generator_start_days: int = Field(
        ..., description="発電機の起動状態 (0: 停止, 1: 起動)"
    )
    generator_stop_days: int = Field(
        ..., description="発電機の停止状態 (0: 停止, 1: 停止)"
    )


class OverallOutput(BaseModel):
    generator_outputs: list[GeneratorOutput] = Field(
        ..., description="全発電機のアウトプット"
    )
    overall_cost: float = Field(..., description="合計コスト (円)")
    overall_output: float = Field(..., description="合計出力 (MW)")
    overall_operation_days: int = Field(..., description="合計稼働日数")
    overall_start_days: int = Field(..., description="合計起動日数")
    overall_stop_days: int = Field(..., description="合計停止日数")
