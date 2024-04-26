"""
EPyT-C Test Part 1
This file is provided to ensure that all functions can be executed correctly using Net3.inp.
"""
from epyt_c.epyt_c_functions import fn 
fn.install("epyt")
from epyt import epanet
d = epanet('Net3.inp') # load Net3.inp
H = d.getComputedHydraulicTimeSeries() # perform hydraulic simulation using EPANET solver
import numpy as np

class TestEpytcFunctions():
    """
    Class to test the functions used in epyt_c_functions.py
    """
    def test_network(self, d):
        """
        Getting basic details of the inp file
        """
        assert fn.network(d)[0] == 97 # count of nodes
        assert fn.network(d)[1] == 119 # count of links
        assert fn.network(d)[2] == 2 # count of reservoirs
        assert fn.network(d)[3] == 3 # count of tanks
        assert fn.network(d)[4] == 2 # count of pumps
        assert fn.network(d)[5] == 0 # count of valves
        assert fn.network(d)[6][2] == '20' # name of the third node
        assert fn.network(d)[7][5] == '103' # name of the sixth link
        assert fn.network(d)[8] == [93, 94] # indices of the two reservoirs
        assert fn.network(d)[9] == [95, 96, 97] # indices of the three tanks
        assert fn.network(d)[10] == [118, 119] # indices of the two pumps
        assert fn.network(d)[11] == [] # indices of the valves (no valves present)
        assert fn.network(d)[12] == 'GPM' # flow unit
        assert fn.network(d)[13][5, 0] == 10 # start node of the sixth link
        assert fn.network(d)[13][5, 1] == 11 # end node of the sixth link
        assert fn.network(d)[14][9, 0] == 1 # true connectivity between 1st and 10th nodes
        assert fn.network(d)[14][10, 0] == 0 # false connectivity between 1st and 11th nodes
        assert fn.network(d)[15][5] == 411.48 # length of the sixth pipe in SI unit (m)
        assert fn.network(d)[16][5] == 406.4 # diameter of the sixth pipe in SI unit (mm)
        assert fn.network(d)[17][5] == 10 # start node of the sixth link
        assert fn.network(d)[18][5] == 11 # end node of the sixth link
        assert fn.network(d)[19] == 0 # count of nodes omitted from the analysis
        assert fn.network(d)[20] == [] # indices of omitted nodes
        assert fn.network(d)[21] == 0 # count of links omitted from the analysis
        assert fn.network(d)[22] == [] # indices of omitted links
        print('Function 1 test - Success')
        
    def test_incoming_links(self, node_id, end_nodes_matrix):
        """
        Getting incoming links of a specific node
        """
        end_nodes_matrix = fn.network(d)[18] # end nodes of every Net3 link
        assert fn.incoming_links(node_id, end_nodes_matrix)[0] == [117] # incoming link to the first node
        print('Function 2 test - Success')
        
    def test_outgoing_links(self, node_id, start_nodes_matrix):
        """
        Getting outgoing links of a specific node
        """
        node_id = 1
        start_nodes_matrix = fn.network(d)[17] # start nodes of every Net3 link
        assert fn.incoming_links(node_id, start_nodes_matrix)[0] == [30] # outgoing link from the second node
        print('Function 3 test - Success')
        
    def test_minimum_link_length(self, steps_count, water_quality_step, pipe_velocity_tolerance, pipe_velocity_matrix):
        """
        Getting minimum length (m) to be specified for pumps and valves
        """
        steps_count = 27 # time steps in the hydraulic report
        water_quality_step = 300 # water quality time step (s)
        pipe_velocity_tolerance = 0.001 # tolerable flow velocity considered (m/s)
        pipe_velocity_matrix = H.Velocity # from EPANET
        assert fn.minimum_link_length(steps_count, water_quality_step, pipe_velocity_tolerance, pipe_velocity_matrix) == 0.3
        print('Function 4 test - Success')
        
    def test_minimum_link_diameter(self, links_count, pumps_count, valves_count, pipe_diameter_matrix):
        """
        Getting minimum diameter (mm) to be specified for pumps and valves
        """
        links_count = fn.network(d)[1]
        pumps_count = fn.network(d)[4]
        valves_count = fn.network(d)[5]
        pipe_diameter_matrix = fn.network(d)[16]
        assert fn.minimum_link_diameter(links_count, pumps_count, valves_count, pipe_diameter_matrix) == 203.2
        print('Function 5 test - Success')
        
    def test_sync_time(self, d, H, water_quality_time, hydraulic_steps_count, base_time_seconds, \
                       hydraulic_simulation_time, day_count, base_time_days, water_quality_step, \
                           expected_hydaulic_step, synchronising_option, reservoir_pattern):
        """
        Synchronizing water quality and hydraulic time steps
        """
        water_quality_time = 86700 # water quality time (s)
        hydraulic_steps_count = 27 # expected total time steps in the hydraulic report
        base_time_seconds = 86400 # base time period (s)
        hydraulic_simulation_time = 86400 # total hydraulic simuation time (s)
        day_count = 2 # count of the day in water quality simulation (86700 s corresponds to 2nd day)
        base_time_days = 1 # base time period (day)
        water_quality_step = 300 # water quality time step (s)
        expected_hydaulic_step = 25 # expected time step in the hydraulic report
        synchronising_option = 'steady'
        """Using dummy data for reservoir pattern"""
        reservoir_pattern = np.zeros((3, 288, 3))
        assert fn.sync_time(d, H, water_quality_time, hydraulic_steps_count, base_time_seconds, \
                       hydraulic_simulation_time, day_count, base_time_days, water_quality_step, \
                           expected_hydaulic_step, synchronising_option, reservoir_pattern) == [25, 25, 287, 287]
        print('Function 6 test - Success')
        
    def test_time_filter(self, H, ratio, hydraulic_steps_count, hydraulic_step):
        """
        Filtering out unwanted time steps from hydraulic analysis output
        """
        ratio = 1.2 # dummy value
        hydraulic_steps_count = 27 # expected total time steps in the hydraulic report
        hydraulic_step = 3600 # hydraulic time step (s)
        assert fn.time_filter(H, ratio, hydraulic_steps_count, hydraulic_step) == [5, 23]
        print('Function 7 test - Success')
        
    def test_time_data(self, time_matrix, filtered_time_step_matrix):
        """
        Cleaning time data
        """
        time_matrix = H.Time # from EPANET
        """Using dummy data for filtered_time_step_matrix"""
        filtered_time_step_matrix = [5, 23]
        assert (fn.time_data(time_matrix, filtered_time_step_matrix) == np.arange(0, 90000, 3600)).all()
        print('Function 8 test - Success')
        
    def test_velocity_data(self, pipe_velocity_matrix, filtered_time_step_matrix, flow_unit):
       """
       Cleaning velocity data
       """ 
       pipe_velocity_matrix = H.Velocity # from EPANET
       """Using dummy data for filtered_time_step_matrix"""
       filtered_time_step_matrix = [5, 23]
       flow_unit = fn.network(d)[12]
       assert (fn.velocity_data(pipe_velocity_matrix, filtered_time_step_matrix, flow_unit)[:, 118] == np.zeros(25)).all()
       print('Function 9 test - Success')
       
    def test_demand_data(self, node_demand_matrix, filtered_time_step_matrix, flow_unit):
       """
       Cleaning demand data
       """
       node_demand_matrix = H.Demand # from EPANET
       """Using dummy data for filtered_time_step_matrix"""
       filtered_time_step_matrix = [5, 23]
       flow_unit = fn.network(d)[12]
       assert (fn.demand_data(node_demand_matrix, filtered_time_step_matrix, flow_unit)[:, 2] == np.zeros(25)).all()
       print('Function 10 test - Success')
       
    def test_flow_data(self, pipe_flow_matrix, filtered_time_step_matrix, flow_unit):
        """
        Cleaning flow data
        """
        pipe_flow_matrix = H.Flow # from EPANET
        """Using dummy data for filtered_time_step_matrix"""
        filtered_time_step_matrix = [5, 23]
        flow_unit = fn.network(d)[12]
        assert (fn.flow_data(pipe_flow_matrix, filtered_time_step_matrix, flow_unit)[5: 22, 118] == np.zeros(17)).all()
        print('Function 11 test - Success')
        
    def test_tank_volume_data(self, tank_volume_matrix, filtered_time_step_matrix, flow_unit):
        """
        Cleaning tank volume data
        """
        tank_volume_matrix = H.TankVolume # from EPANET
        """Using dummy data for filtered_time_step_matrix"""
        filtered_time_step_matrix = [5, 23]
        flow_unit = fn.network(d)[12]
        assert (fn.tank_volume_data(tank_volume_matrix, filtered_time_step_matrix, flow_unit)[:, 94: 97] != 0).any()
        print('Function 12 test - Success')
        
    def test_maximum_segments(self, pipe_velocity_tolerance, water_quality_step, link_length_matrix, pipe_velocity_matrix):
        """
        Determining the maximum number of segments for pipe discretization
        """
        pipe_velocity_tolerance = 0.001 # tolerable flow velocity considered (m/s)
        water_quality_step = 300 # water quality time step (s)
        link_length_matrix = fn.network(d)[15]
        pipe_velocity_matrix = H.Velocity # from EPANET
        assert fn.maximum_segments(pipe_velocity_tolerance, water_quality_step, link_length_matrix, pipe_velocity_matrix) == 102
        print('Function 13 test - Success')
        
    def test_reservoir_names(self, reservoirs_count, node_names, reservoir_index_matrix):
        """
        Display the names of reservoirs
        """
        reservoirs_count = fn.network(d)[2]
        node_names = fn.network(d)[6]
        reservoir_index_matrix = fn.network(d)[8]
        assert fn.reservoir_names(reservoirs_count, node_names, reservoir_index_matrix) != ''
        print('Function 14 test - Success')
        
    def test_tank_names(self, tanks_count, node_names, tank_index_matrix):
        """
        Display the names of tanks
        """
        tanks_count = fn.network(d)[3]
        node_names = fn.network(d)[6]
        tank_index_matrix = fn.network(d)[9]
        assert fn.tank_names(tanks_count, node_names, tank_index_matrix) != ''
        print('Function 15 test - Success')
        
    def test_pump_names(self, pumps_count, valves_count, link_names):
        """
        Display the names of pumps
        """
        pumps_count = fn.network(d)[4]
        valves_count = fn.network(d)[5]
        link_names = fn.network(d)[7]
        assert fn.pump_names(pumps_count, valves_count, link_names) != ''
        print('Function 16 test - Success')
        
    def test_valve_names(self, valves_count, link_names):
        """
        Display the names of valves
        """
        valves_count = fn.network(d)[5]
        link_names = fn.network(d)[7]
        assert fn.valve_names(valves_count, link_names) == None
        print('Function 17 test - Success')
        
    def test_simulation_info(self, maximum_iterations_count, water_quality_time_days, water_quality_step, total_water_quality_steps):
        """
        Display simulation information
        """
        maximum_iterations_count = 200 # times for which the water qality simulation will be iteratively performed
        water_quality_time_days = 10 # days for which water quality will be simulated
        water_quality_step = 300 # water quality time step (s)
        total_water_quality_steps = 2881 # total water quality steps involved
        assert fn.simulation_info(maximum_iterations_count, water_quality_time_days, water_quality_step, total_water_quality_steps) != ''
        print('Function 18 test - Success')
        
    def test_msrt_info(self, quality_parameters_count, bulk_quality_parameters_count, wall_quality_parameters_count):
        """
        Display MSRT model information
        """
        """Using dummy data for quality_parameters_count"""
        quality_parameters_count = 3
        """Using dummy data for bulk_quality_parameters_count"""
        bulk_quality_parameters_count = 3
        """Using dummy data for wall_quality_parameters_count"""
        wall_quality_parameters_count = 0
        assert fn.msrt_info(quality_parameters_count, bulk_quality_parameters_count, wall_quality_parameters_count) != ''
        print('Function 19 test - Success')
        
    def test_omitted_nodes(self, omitted_nodes_count, node_names, omitted_node_index_matrix):
        """
        Display nodes omitted from analysis
        """
        omitted_nodes_count = fn.network(d)[19]
        node_names = fn.network(d)[6]
        omitted_node_index_matrix = fn.network(d)[20]
        assert fn.omitted_nodes(omitted_nodes_count, node_names, omitted_node_index_matrix) == None
        print('Function 20 test - Success')
        
    def test_omitted_links(self, omitted_links_count, link_names, omitted_link_index_matrix):
        """
        Display links omitted from analysis
        """
        omitted_links_count = fn.network(d)[21]
        link_names = fn.network(d)[7]
        omitted_link_index_matrix = fn.network(d)[22]
        assert fn.omitted_links(omitted_links_count, link_names, omitted_link_index_matrix) == None
        print('Function 21 test - Success')
        
test = TestEpytcFunctions()
test.test_network(d)
test.test_incoming_links(0, fn.network(d)[18])
test.test_outgoing_links(1, fn.network(d)[17])
test.test_minimum_link_length(27, 300, 0.001, H.Velocity)
test.test_minimum_link_diameter(fn.network(d)[1], fn.network(d)[4], fn.network(d)[5], fn.network(d)[16])
test.test_sync_time(d, H, 86700, 27, 86400,86400, 2, 1, 300, 25, 'steady', np.zeros((3, 288, 3)))
test.test_time_filter(H, 1.2, 27, 3600)
test.test_time_data(H.Time, [5, 23])
test.test_velocity_data(H.Velocity, [5, 23], 'GPM')
test.test_demand_data(H.Demand, [5, 23], 'GPM')
test.test_flow_data(H.Flow, [5, 23], 'GPM')
test.test_tank_volume_data(H.TankVolume, [5, 23], 'GPM')
test.test_maximum_segments(0.001, 300, fn.network(d)[15], H.Velocity)
test.test_reservoir_names(fn.network(d)[2], fn.network(d)[6], fn.network(d)[8])
test.test_tank_names(fn.network(d)[3], fn.network(d)[6], fn.network(d)[9])
test.test_pump_names(fn.network(d)[4], fn.network(d)[5], fn.network(d)[7])
test.test_valve_names(fn.network(d)[5], fn.network(d)[7])
test.test_simulation_info(200, 10, 300, 2881)
test.test_msrt_info(3, 3, 0)
test.test_omitted_nodes(fn.network(d)[19], fn.network(d)[6], fn.network(d)[20])
test.test_omitted_links(fn.network(d)[21], fn.network(d)[7], fn.network(d)[22])

print('\nAll tests completed!\n')

