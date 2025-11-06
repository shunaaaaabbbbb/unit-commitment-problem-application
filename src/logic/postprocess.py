from src.models.solver import Solver
from src.schemas.data_schema import DailySchedule, StructuredOutput
from src.utils.safe_cast import ensure_type


def create_schedules(solver: Solver) -> list[DailySchedule]:
    schedules = []
    for t in range(solver.num_timeseries):
        for p in range(solver.num_units):
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
                generator_id=solver.generator_parameters[p].generator_id,
                start=start,
                stop=stop,
                operation=operation,
                output=output,
                cost=cost,
            )
            schedules.append(schedule)
    return schedules


def create_structured_output(schedules: list[DailySchedule]) -> StructuredOutput:
    total_cost = sum(schedule.cost for schedule in schedules)
    total_output = sum(schedule.output for schedule in schedules)
    total_operation_days = sum(schedule.operation for schedule in schedules)
    total_start_days = sum(schedule.start for schedule in schedules)
    total_stop_days = sum(schedule.stop for schedule in schedules)
    return StructuredOutput(
        schedules=schedules,
        total_cost=total_cost,
        total_output=total_output,
        total_operation_days=total_operation_days,
        total_start_days=total_start_days,
        total_stop_days=total_stop_days,
    )
