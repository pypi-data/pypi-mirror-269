import os
from .run import run_epytc
from dataclasses import dataclass
from hydra.utils import instantiate
from omegaconf import OmegaConf


@dataclass
class epytc_class:
    module: str
    maximum_iterations_required: int
    simulation_period_days: int
    simulation_time_step: int
    base_period_days: int
    minimum_pipe_flow_velocity: float
    reservoir_quality_matrix: list[list[float]]
    reservoir_quality_pattern: str
    reservoir_quality_pattern_random_variability: float
    reservoir_injection_pattern: str
    reservoir_injection_pattern_random_variability: float
    reservoir_injection_start_time: list[list[float]]
    reservoir_injection_end_time: list[list[float]]
    reservoir_injection_input_value: list[list[float]]
    injection_nodes_index: list
    injection_nodes_quality_matrix: list[list[float]]
    injection_node_quality_pattern: str
    injection_node_quality_pattern_random_variability: float
    injection_node_injection_pattern: str
    injection_node_injection_pattern_random_variability: float
    injection_node_injection_start_time: list[list[float]]
    injection_node_injection_end_time: list[list[float]]
    injection_node_injection_input_value: list[list[float]]
    hyd_wq_sync_option: str


def create_epytc():
    """Creates an object of dataclass epytc-class

    :return: An epytc_class object
    :rtype: epytc_class
    """
    print("Creating instance of EPyT-C with default values")
    file_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = OmegaConf.load(os.path.join(file_dir, "default_values.yaml"))
    epytc = instantiate(default_config.epytc_class)

    return epytc


def execute_epytc(epytc: epytc_class):
    """Execute the epytc module

    :param epytc: epytc object
    :type epytc: epytc_class
    """
    print("EPyT-C loaded for execution...")
    run_epytc(epytc)
