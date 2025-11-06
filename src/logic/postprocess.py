from src.models.solver import Solver
from src.schemas.data_schema import DailySchedule, StructuredOutput


def create_schedules(solver: Solver) -> list[DailySchedule]:
    schedules = []
    for t in range(solver.num_timeseries):
        for p in range(solver.num_units):
            start = int(solver.start[t, p].value())
            stop = int(solver.stop[t, p].value())
            operation = int(solver.operation[t, p].value())
            output = float(solver.output[t, p].value())
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
