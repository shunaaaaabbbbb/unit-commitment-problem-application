from src.models.solver import Solver
from src.schemas.data_schema import InputData


def run_optimization(input_data: InputData) -> Solver:
    solver = Solver(input_data)
    solver.build_model()
    solver.solve()
    return solver
