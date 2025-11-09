from src.models.solver import Solver
from src.schemas.data_schema import DailySchedule, GeneratorOutput, OverallOutput
from src.utils.safe_cast import ensure_type


def create_schedules(p: int, solver: Solver) -> list[DailySchedule]:
    schedules = []
    for t in range(solver.num_timeseries):
        start = ensure_type(solver.start[t, p].value(), int)
        stop = ensure_type(solver.stop[t, p].value(), int)
        operation = ensure_type(solver.operation[t, p].value(), int)
        output = ensure_type(solver.output[t, p].value(), float)
        cost = (
            solver.cost_runs[p] * output
            + solver.cost_starts[p] * start
            + solver.cost_stops[p] * stop
        )
        schedule = DailySchedule(
            date=solver.timeseries[t].date,
            start=start,
            stop=stop,
            operation=operation,
            output=output,
            cost=cost,
        )
        schedules.append(schedule)

    return schedules


def create_generator_output(
    generator_id: str, schedules: list[DailySchedule]
) -> GeneratorOutput:
    generator_cost = sum(schedule.cost for schedule in schedules)
    generator_output = sum(schedule.output for schedule in schedules)
    generator_operation_days = sum(schedule.operation for schedule in schedules)
    generator_start_days = sum(schedule.start for schedule in schedules)
    generator_stop_days = sum(schedule.stop for schedule in schedules)
    return GeneratorOutput(
        generator_id=generator_id,
        schedules=schedules,
        generator_cost=generator_cost,
        generator_output=generator_output,
        generator_operation_days=generator_operation_days,
        generator_start_days=generator_start_days,
        generator_stop_days=generator_stop_days,
    )


def create_overall_output(generator_outputs: list[GeneratorOutput]) -> OverallOutput:
    overall_cost = sum(
        generator_output.generator_cost for generator_output in generator_outputs
    )
    overall_output = sum(
        generator_output.generator_output for generator_output in generator_outputs
    )
    overall_operation_days = sum(
        generator_output.generator_operation_days
        for generator_output in generator_outputs
    )
    overall_start_days = sum(
        generator_output.generator_start_days for generator_output in generator_outputs
    )
    overall_stop_days = sum(
        generator_output.generator_stop_days for generator_output in generator_outputs
    )
    return OverallOutput(
        generator_outputs=generator_outputs,
        overall_cost=overall_cost,
        overall_output=overall_output,
        overall_operation_days=overall_operation_days,
        overall_start_days=overall_start_days,
        overall_stop_days=overall_stop_days,
    )
