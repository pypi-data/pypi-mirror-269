"""
EPyT-C Test Part 2
This file is provided to ensure that all functions can be executed correctly using Net3.inp 
and MSRT-1: Chlorine decay and trihalomethanes formation module.
"""
from epyt_c.epyt_c_functions import fn 
fn.install("epyt")
from epyt import epanet
d = epanet('Net3.inp') # load Net3.inp
from epyt_c.chlorine_decay_thms_formation import module
import numpy as np

class TestEpytcModule1():
    """
    Class to test the functions used in chlorine_decay_thms_formation.py
    """
    def test_details(self):
        """
        Display modulde details
        """
        assert module.details() != ''
        print('Function 1 test - Success')
        
    def test_network(self, d):
        """
        Getting basic details of the network
        """
        assert module.network(d)[0] == 97 # count of nodes
        assert module.network(d)[1] == 119 # count of links
        assert module.network(d)[2] == 2 # count of reservoirs
        assert module.network(d)[3] == 3 # count of tanks
        assert module.network(d)[4] == 2 # count of pumps
        assert module.network(d)[5] == 0 # count of valves
        assert module.network(d)[6][2] == '20' # name of the third node
        assert module.network(d)[7][5] == '103' # name of the sixth link
        assert module.network(d)[8] == [93, 94] # indices of the two reservoirs
        assert module.network(d)[9] == [95, 96, 97] # indices of the three tanks
        assert module.network(d)[10] == [118, 119] # indices of the two pumps
        assert module.network(d)[11] == [] # indices of the valves (no valves present)
        assert module.network(d)[12] == 'GPM' # flow unit
        assert module.network(d)[13][5, 0] == 10 # start node of the sixth link
        assert module.network(d)[13][5, 1] == 11 # end node of the sixth link
        assert module.network(d)[14][9, 0] == 1 # true connectivity between 1st and 10th nodes
        assert module.network(d)[14][10, 0] == 0 # false connectivity between 1st and 11th nodes
        assert module.network(d)[15][5] == 411.48 # length of the sixth pipe in SI unit (m)
        assert module.network(d)[16][5] == 406.4 # diameter of the sixth pipe in SI unit (mm)
        assert module.network(d)[17][5] == 10 # start node of the sixth link
        assert module.network(d)[18][5] == 11 # end node of the sixth link
        assert module.network(d)[19] == 0 # count of nodes omitted from the analysis
        assert module.network(d)[20] == [] # indices of omitted nodes
        assert module.network(d)[21] == 0 # count of links omitted from the analysis
        assert module.network(d)[22] == [] # indices of omitted links
        print('Function 2 test - Success')
        
    def test_species(self):
        """
        Defining the species information of the MSRT module selected
        """
        assert module.species()[0] == 3 # count of water quality parameters
        assert module.species()[1] == 3 # count of bulk water quality parameters
        assert module.species()[2] == 0 # count of wall water quality parameters
        assert module.species()[3] == 9 # count of model variables
        print('Function 3 test - Success')
        
    def test_zero_order_reaction(self, water_quality_step):
        """
        Defining zero-order reaction
        """
        water_quality_step = 300 # water quality time step (s)
        assert module.zero_order_reaction(water_quality_step) == 300
        print('Function 4 test - Success')
        
    def test_first_order_reaction(self, reaction_rate_constant, concentration_value, water_quality_step):
        """
        Defining first-order reaction
        Using dummy data
        """
        reaction_rate_constant = -1e-3 # (1/s)
        concentration_value = 1 # (mg/L)
        water_quality_step = 300 # water quality time step (s)
        assert round(module.first_order_reaction(reaction_rate_constant, concentration_value, water_quality_step), 1) == -0.2
        print('Function 5 test - Success')
        
    def test_Reynolds_number(self, pipe_velocity, pipe_diameter, kinematic_viscosity):
        """
        Defining Reynolds number
        Using dummy data
        """
        pipe_velocity = 0.2 # (m/s)
        pipe_diameter = 200 # (mm)
        kinematic_viscosity = 9.31e-7 # (sq.m/s)
        assert round(module.Reynolds_number(pipe_velocity, pipe_diameter, kinematic_viscosity)) == 42965
        print('Function 6 test - Success')
        
    def test_Schmidt_number(self, kinematic_viscosity, molecular_diffusivity):
        """
        Defining Schmidt number
        Using dummy data
        """
        kinematic_viscosity = 9.31e-7 # (sq.m/s)
        molecular_diffusivity = 12.5e-10 # (sq.m/s)
        assert round(module.Schmidt_number(kinematic_viscosity, molecular_diffusivity)) == 745
        print('Function 7 test - Success')
        
    def test_Sherwood_number(self, Reynolds_number, Schmidt_number, pipe_diameter, pipe_length):
        """
        Defining Sherwood number
        Using dummy data
        """
        Reynolds_number = 42965
        Schmidt_number = 745
        pipe_diameter = 200 # (mm)
        pipe_length = 1000 # (m)
        assert round(module.Sherwood_number(Reynolds_number, Schmidt_number, pipe_diameter, pipe_length)) == 33
        print('Function 8 test - Success')
        
    def test_mass_transfer_coefficient(self, Sherwood_number, molecular_diffusivity, pipe_diameter):
        """
        Defining Mass transfer coefficient
        Using dummy data
        """
        Sherwood_number = 33
        molecular_diffusivity = 12.5e-10 # (sq.m/s)
        pipe_diameter = 200 # (mm)
        assert round(module.mass_transfer_coefficient(Sherwood_number, molecular_diffusivity, pipe_diameter), 7) == 2e-7
        print('Function 9 test - Success')
                             
    def test_hydraulic_mean_radius(self, pipe_diameter):
        """
        Defining Defining Hydrauic mean radius
        Using dummy data
        """
        pipe_diameter = 200 # (mm)
        assert module.hydraulic_mean_radius(pipe_diameter) == 0.05
        print('Function 10 test - Success')
        
    def test_variables(self, maximum_iterations_count, variables_count):
        """
        Defining variables of the MSRT module
        """
        maximum_iterations_count = 200 # times for which the water qality simulation will be iteratively performed
        variables_count = 9 # count of selected MSRT model variables
        assert (module.variables(maximum_iterations_count, variables_count)[:, 0] > 0).all()
        assert np.logical_and(5.2e-6 <= module.variables(maximum_iterations_count, variables_count)[:, 1], \
                       module.variables(maximum_iterations_count, variables_count)[:, 1] <= 3.4e-3).all()
        assert np.logical_and(1.04e-7 <= module.variables(maximum_iterations_count, variables_count)[:, 2], \
                       module.variables(maximum_iterations_count, variables_count)[:, 2] <= 1.43e-5).all()
        assert np.logical_and(0.15 <= module.variables(maximum_iterations_count, variables_count)[:, 3], \
                       module.variables(maximum_iterations_count, variables_count)[:, 3] <= 2.50).all()
        assert np.logical_and(5.68 <= module.variables(maximum_iterations_count, variables_count)[:, 4], \
                       module.variables(maximum_iterations_count, variables_count)[:, 4] <= 188.2).all()
        assert (module.variables(maximum_iterations_count, variables_count)[:, 5] == 12.5e-10).all()
        assert np.logical_and(7.8e-10 <= module.variables(maximum_iterations_count, variables_count)[:, 6], \
                       module.variables(maximum_iterations_count, variables_count)[:, 6] <= 11.5e-10).all()
        assert (module.variables(maximum_iterations_count, variables_count)[:, 7] == 8.8e-10).all()
        assert (module.variables(maximum_iterations_count, variables_count)[:, 8] == 9.31e-7).all()
        print('Function 11 test - Success')
        
    def test_pipe_reaction(self, water_quality_step, pipe_number, grid_number, pipe_velocity, pipe_diameter,\
                           pipe_length, pipe_segment_width, variables_matrix, pipe_concentration_matrix):
        """
        Defining pipe reactions for the MSRT model selected
        Using dummy data
        """
        water_quality_step = 300 # water quality time step (s)
        pipe_number = 1 # 2nd pipe is considered
        grid_number = 2 # 3rd grid
        pipe_velocity = 0.5 # (m/s)
        pipe_diameter = 200 # (mm)
        pipe_length = 1000 # (m)
        pipe_segment_width = 16.667 # (m)
        variables_matrix = module.variables(200, 9)[2] # Variable values corresponding to 3rd iteration
        pipe_concentration_matrix = np.ones((3, 5, 119)) # Assuming the maxiumum segments is 5
        assert (module.pipe_reaction(water_quality_step, pipe_number, grid_number, pipe_velocity, pipe_diameter, \
                             pipe_length, pipe_segment_width, variables_matrix, pipe_concentration_matrix)[0] <= 0)
        assert (module.pipe_reaction(water_quality_step, pipe_number, grid_number, pipe_velocity, pipe_diameter, \
                                 pipe_length, pipe_segment_width, variables_matrix, pipe_concentration_matrix)[1] <= 0)
        assert (module.pipe_reaction(water_quality_step, pipe_number, grid_number, pipe_velocity, pipe_diameter, \
                                 pipe_length, pipe_segment_width, variables_matrix, pipe_concentration_matrix)[2] >= 0)
        print('Function 12 test - Success')
        
    def test_tank_reaction(self, water_quality_step, water_quality_step_number, tank_number, tank_volume_previous_step,\
                           tank_volume_current, variables_matrix, initial_node_concentration_matrix, node_concentration_matrix):
       """
       Defining tank reactions for the MSRT model selected
       Using dummy data
       """
       water_quality_step = 300 # water quality time step (s)
       water_quality_step_number = 10 # 10th step of simulation
       tank_number = 96 # 97th node or 3rd tank
       tank_volume_previous_step = 19358 # tank volume in cu.m for the previous step
       tank_volume_current = 20172 # current tank volume in cu.m
       variables_matrix = module.variables(200, 9)[2] # Variable values corresponding to 3rd iteration
       initial_node_concentration_matrix = np.zeros((97, 3))
       node_concentration_matrix = np.ones((3, 2881, 97))
       assert (module.tank_reaction(water_quality_step, water_quality_step_number, tank_number, tank_volume_previous_step,\
                              tank_volume_current, variables_matrix, initial_node_concentration_matrix, \
                                  node_concentration_matrix)[0] <= 0)
       assert (module.tank_reaction(water_quality_step, water_quality_step_number, tank_number, tank_volume_previous_step,\
                             tank_volume_current, variables_matrix, initial_node_concentration_matrix, \
                                 node_concentration_matrix)[1] <= 0)
       assert (module.tank_reaction(water_quality_step, water_quality_step_number, tank_number, tank_volume_previous_step,\
                           tank_volume_current, variables_matrix, initial_node_concentration_matrix, \
                               node_concentration_matrix)[2] >= 0)
       print('Function 13 test - Success')
       
    def test_reservoir_quality(self, d, maximum_iterations_count, source_quality_matrix, pattern_input_command1, \
                               percentage_variation_random_pattern1):
        """
        Defining source quality at the reservoir(s)
        Using dummy data
        """
        maximum_iterations_count = 200 # times for which the water qality simulation will be iteratively performed
        source_quality_matrix = [[1, 1, 0],[1, 1, 0]] # quality at the two sources of Net3 (boundary condition)
        pattern_input_command1 = 'none', 'rand' 
        percentage_variation_random_pattern1 = 0, 0.2 # 0 and 20% variations
        
        val = module.reservoir_quality(d, maximum_iterations_count, source_quality_matrix, pattern_input_command1[0], \
                                 percentage_variation_random_pattern1[0])
        assert (val[0] == source_quality_matrix[0]).all()
        assert (val[1] == source_quality_matrix[1]).all()
        
        val = module.reservoir_quality(d, maximum_iterations_count, source_quality_matrix, pattern_input_command1[1], \
                                 percentage_variation_random_pattern1[1])
        assert np.logical_and(0.8 <= val[0][:, 0], val[0][:, 0] <= 1.2).all()    
        assert np.logical_and(0.8 <= val[0][:, 1], val[0][:, 1] <= 1.2).all()
        assert np.logical_and(0.8 <= val[1][:, 0], val[1][:, 0] <= 1.2).all()
        assert np.logical_and(0.8 <= val[1][:, 1], val[1][:, 0] <= 1.2).all()
        print('Function 14 test - Success')
        
    def test_reservoir_pattern(self, d, base_time_days, pattern_input_command2, percentage_variation_random_pattern2, \
                               reservoir_injection_start_step, reservoir_injection_end_step, reservoir_injection_input):
        """
        Defining source quality pattern for the reservoir(s)
        Using dummy data
        """
        base_time_days = 1 # base time period (day)
        pattern_input_command2 = 'none', 'rand', 'specific'
        percentage_variation_random_pattern2 = 0, 0.2 # 0 and 20% variations
        reservoir_injection_start_step = [[0],[12]] # injection for first an second source nodes start at 0th and 12th h, respectively
        reservoir_injection_end_step = [[12], [24]] # injection for first an second source nodes end at 12th and 24th h, respectively
        reservoir_injection_input = [[1], [1]] # value to multiply the source quality
        
        val = module.reservoir_pattern(d, base_time_days, pattern_input_command2[0], percentage_variation_random_pattern2[0], \
                                   reservoir_injection_start_step, reservoir_injection_end_step, reservoir_injection_input)
        assert (val[0] == [1, 1, 1]).all()
        assert (val[1] == [1, 1, 1]).all()
        
        val = module.reservoir_pattern(d, base_time_days, pattern_input_command2[1], percentage_variation_random_pattern2[1], \
                                   reservoir_injection_start_step, reservoir_injection_end_step, reservoir_injection_input)
        assert np.logical_and(0.8 <= val, val <= 1.2).all()
        
        val = module.reservoir_pattern(d, base_time_days, pattern_input_command2[2], percentage_variation_random_pattern2[1], \
                                   reservoir_injection_start_step, reservoir_injection_end_step, reservoir_injection_input)
        assert (val[0][reservoir_injection_start_step[0][0]: reservoir_injection_end_step[0][0]] == reservoir_injection_input[0][0]).all()
        assert (val[0][reservoir_injection_start_step[1][0]: reservoir_injection_end_step[1][0]] == 0).all()
        assert (val[1][reservoir_injection_start_step[0][0]: reservoir_injection_end_step[0][0]] == 0).all()
        assert (val[1][reservoir_injection_start_step[1][0]: reservoir_injection_end_step[1][0]] == reservoir_injection_input[0][0]).all()
        print('Function 15 test - Success')
        
    def test_injection_quality(self, maximum_iterations_count, injection_node_index_matrix, injection_node_quality_matrix, \
                               pattern_input_command1, percentage_variation_random_pattern1):
        """
        Defining quality at the injection node(s)
        Using dummy data
        """
        maximum_iterations_count = 200 # times for which the water qality simulation will be iteratively performed
        injection_node_index_matrix = [21] # node with index 21 is specified as injection node
        injection_node_quality_matrix = [[2, 0, 0]] # # quality at the injection node of Net3 (boundary condition)
        pattern_input_command1 = 'none', 'rand' 
        percentage_variation_random_pattern1 = 0, 0.2 # 0 and 20% variations
        val = module.injection_quality(maximum_iterations_count, injection_node_index_matrix, injection_node_quality_matrix, \
                                   pattern_input_command1[0], percentage_variation_random_pattern1[0])
        assert (val == injection_node_quality_matrix[0]).all()
        
        val = module.injection_quality(maximum_iterations_count, injection_node_index_matrix, injection_node_quality_matrix, \
                                   pattern_input_command1[1], percentage_variation_random_pattern1[1])
        assert np.logical_and(1.6 <= val[0][:, 0], val[0][:, 0] <= 2.4).all()
        assert (val[0][:,1: 2] == 0).all()
        print('Function 16 test - Success')
        
    def test_injection_pattern(self, d, base_time_days, injection_node_index_matrix, pattern_input_command2, percentage_variation_random_pattern2,\
                               injection_node_injection_start_step, injection_node_injection_end_step, injection_node_injection_input):
        """
        Defining injection pattern for the injection node(s)
        Using dummy data
        """
        base_time_days = 1 # base time period (day)
        injection_node_index_matrix = [21] # node with index 21 is specified as injection node
        pattern_input_command2 = 'none', 'rand', 'specific'
        percentage_variation_random_pattern2 = 0, 0.2 # 0 and 20% variations
        injection_node_injection_start_step = [[3]] # injection for injection node start at 3rd h
        injection_node_injection_end_step = [[19]] # injection for injection node end at 19th h
        injection_node_injection_input = [[1]] # value to multiply the injection node quality
        
        val = module.injection_pattern(d, base_time_days, injection_node_index_matrix, pattern_input_command2[0], percentage_variation_random_pattern2[0],\
                                   injection_node_injection_start_step, injection_node_injection_end_step, injection_node_injection_input)
        assert (val == [1, 1, 1]).all()
        
        val = module.injection_pattern(d, base_time_days, injection_node_index_matrix, pattern_input_command2[1], percentage_variation_random_pattern2[1],\
                                   injection_node_injection_start_step, injection_node_injection_end_step, injection_node_injection_input)
        assert np.logical_and(0.8 <= val, val <= 1.2).all()
        
        val = module.injection_pattern(d, base_time_days, injection_node_index_matrix, pattern_input_command2[2], percentage_variation_random_pattern2[1],\
                                   injection_node_injection_start_step, injection_node_injection_end_step, injection_node_injection_input)
        assert (val[injection_node_injection_start_step[0][0]: injection_node_injection_end_step[0][0]] == injection_node_injection_input[0][0]).all()
        assert (val[: injection_node_injection_start_step[0][0], 0] == 0).all()
        assert (val[injection_node_injection_end_step[0][0] :, 0] == 0).all()
        print('Function 17 test - Success')

test = TestEpytcModule1()
test.test_details()
test.test_network(d)
test.test_species()
test.test_zero_order_reaction(300)
test.test_first_order_reaction(1e-3, 1, 300)
test.test_Reynolds_number(0.2, 200, 9.31e-7)
test.test_Schmidt_number(9.31e-7, 12.5e-10)
test.test_Sherwood_number(42965, 745, 200, 1000)
test.test_mass_transfer_coefficient(33, 12.5e-10, 200)
test.test_hydraulic_mean_radius(200)
test.test_variables(200, 9)
test.test_pipe_reaction(300, 1, 2, 0.5, 200, 100, 16.667, module.variables(200, 9)[2], np.ones((3, 5, 119)))
test.test_tank_reaction(300, 10, 96, 19358, 20172, module.variables(200, 9)[2], np.zeros((97, 3)), np.ones((3, 2881, 97)))
test.test_reservoir_quality(d, 200, [[1, 1, 0],[1, 1, 0]], ('none', 'rand'), (0, 0.2))
test.test_reservoir_pattern(d, 1, ('none', 'rand', 'specific'), (0, 0.2), [[0],[12]], [[12], [24]], [[1], [1]])
test.test_injection_quality(200, [21], [[2, 0, 0]], ('none', 'rand'), (0, 0.2))
test.test_injection_pattern(d, 1, [21], ('none', 'rand', 'specific'), (0, 0.2), [[3]], [[19]], [[1]])

print('\nAll tests completed!\n')
