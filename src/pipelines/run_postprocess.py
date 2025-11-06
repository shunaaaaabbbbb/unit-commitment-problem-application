from src.logic.postprocess import create_schedules, create_structured_output
from src.models.solver import Solver
from src.schemas.data_schema import StructuredOutput


def run_postprocess(model_output: Solver) -> StructuredOutput:
    schedules = create_schedules(model_output)
    structured_output = create_structured_output(schedules)
    return structured_output
