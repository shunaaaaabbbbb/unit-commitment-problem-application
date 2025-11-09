from src.logic.visualize import visualize_generations
from src.schemas.data_schema import OverallOutput


def create_output(overall_output: OverallOutput, output_dir: str) -> None:
    visualize_generations(overall_output, output_dir)
