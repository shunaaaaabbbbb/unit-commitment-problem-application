from src.logic.postprocess import (
    create_generator_output,
    create_overall_output,
    create_schedules,
)
from src.models.solver import Solver
from src.schemas.data_schema import InputData, OverallOutput


def run_postprocess(model_output: Solver, input_data: InputData) -> OverallOutput:
    num_units = len(input_data.generator_parameters)
    generator_outputs = []
    for p in range(num_units):
        schedules = create_schedules(p, model_output)
        generator_id = input_data.generator_parameters[p].generator_id
        generator_output = create_generator_output(generator_id, schedules)
        generator_outputs.append(generator_output)
    overall_output = create_overall_output(generator_outputs)
    return overall_output
