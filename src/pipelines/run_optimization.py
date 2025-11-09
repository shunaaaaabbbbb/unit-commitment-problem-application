from src.models.solver import Solver
from src.schemas.data_schema import InputData


def run_optimization(input_data: InputData, output_dir: str) -> Solver:
    solver = Solver(input_data)
    solver.build_model()
    solver.solve(output_dir)
    return solver
