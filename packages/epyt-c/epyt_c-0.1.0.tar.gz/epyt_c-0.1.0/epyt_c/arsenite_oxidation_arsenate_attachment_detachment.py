# Arsenite oxidation and arsenate attachment/detachment module
# Reactive species (bulk) - Aqueous arsenite (mg/L), Aqueous arsenate (mg/L), Aqueous arsenic (mg/L), Residual chlorine (mg/L), and Total organic carbon (mg/L)
# Reactive species (wall) - Adsorbed arsenate (mg/sq.m)

import math
import random
import numpy as np


class module:
    # Display modulde details
    def details():
        print("Arsenite oxidation and arsenate attachemnt/detachment module loaded.")
        print("\nReactive species (bulk):")
        print(
            "Aqueous arsenite (mg/L)\nAqueous arsenate (mg/L)\nAqueous arsenic (mg/L)\
              \nResidual chlorine (mg/L)\nTotal organic carbon (mg/L)"
        )
        print("\nReactive species (wall):")
        print("Adsorbed arsenate (mg/sq.m)")

    # Getting basic details of the network
    def network(d):
        network_info = [
            d.getNodeCount(),
            d.getLinkCount(),
            d.getNodeReservoirCount(),
            d.getNodeTankCount(),
            d.getLinkPumpCount(),
            d.getLinkValveCount(),
            d.getNodeNameID(),
            d.getLinkNameID(),
            d.getNodeReservoirIndex(),
            d.getNodeTankIndex(),
        ]
        index_pumps = []
        for x in range(
            d.getLinkCount() - (d.getLinkPumpCount() + d.getLinkValveCount()),
            len(d.getLinkNameID()) - d.getLinkValveCount(),
        ):
            index_pumps.append(x + 1)
        network_info.append(index_pumps)
        index_valves = []
        for x in range(d.getLinkCount() - d.getLinkValveCount(), len(d.getLinkNameID())):
            index_valves.append(x + 1)
        network_info.append(index_valves)
        network_info.extend(
            [
                d.getFlowUnits(),
                d.getNodesConnectingLinksIndex(),
                d.getConnectivityMatrix(),
            ]
        )
        # Conversion of GPM units to SI units
        if d.getFlowUnits() == "GPM":
            network_info.append(0.3048 * d.getLinkLength())
            network_info.append(25.4 * d.getLinkDiameter())
        else:
            network_info.extend([d.getLinkLength(), d.getLinkDiameter()])
        start_node_matrix = []
        end_node_matrix = []
        for x in range(d.getLinkCount()):
            var1 = d.getNodesConnectingLinksIndex()[x][0]
            var2 = d.getNodesConnectingLinksIndex()[x][1]
            start_node_matrix.append(var1)
            end_node_matrix.append(var2)
        network_info.extend([start_node_matrix, end_node_matrix])
        # Number of nodes omitted for analysis, if any
        number_omitted_nodes = 0
        # Index of omitted nodes
        index_omitted_nodes = []
        # Number of links omitted for analysis, if any
        number_omitted_links = 0
        # Index of omitted nodes
        index_omitted_links = []
        network_info.extend(
            [
                number_omitted_nodes,
                index_omitted_nodes,
                number_omitted_links,
                index_omitted_links,
            ]
        )
        return network_info

    # Defining the species information of the MSRT module selected
    def species():
        msrt_info = []
        number_water_quality_parameters = 6
        msrt_info.append(number_water_quality_parameters)
        number_bulk_water_quality_parameters = 5
        msrt_info.append(number_bulk_water_quality_parameters)
        number_wall_water_quality_parameters = 1
        msrt_info.append(number_wall_water_quality_parameters)
        number_model_variables = 14
        msrt_info.append(number_model_variables)
        msrt_info = [
            number_water_quality_parameters,
            number_bulk_water_quality_parameters,
            number_wall_water_quality_parameters,
            number_model_variables,
        ]
        return msrt_info

    # Defining zero order reaction
    def zero_order_reaction(num1):
        # num1 - water quality time step
        delta_zero_order = num1
        return delta_zero_order

    # Defining first order reaction
    def first_order_reaction(num1, num2, num3):
        # num1 - reaction rate constant; num2 - concentration value; num3 - water quality time step
        m1 = num1 * num1
        m2 = num1 * (num2 + (num3 / 4) * m1)
        m3 = num1 * (num2 + (num3 / 4) * m2)
        m4 = num1 * (num2 + (num3 / 2) * m3)
        delta_first_order = (num3 / 6) * (m1 + 2 * m2 + 2 * m3 + m4)
        return delta_first_order

    # Defining Reynolds number
    def Reynolds_number(num1, num2, num3):
        # num1 - pipe flow velocity (m/s); num2 - pipe diameter (mm); num3 - kinematic viscosity of water (sq.m/s)
        num4 = num2 * 1e-3
        reynolds_num = (num1 * num4) / num3
        return reynolds_num

    # Defining Schmidt number
    def Schmidt_number(num1, num2):
        # num1 - kinematic viscosity of water (sq.m/s); num2 - molecular diffusivity of bulk species (sq.m/s)
        schmidt_num = num1 / num2
        return schmidt_num

    # Defining Sherwood number
    def Sherwood_number(num1, num2, num3, num4):
        # num1 - Reynolds number; num2 - Schmidt number; num3 - pipe diameter (mm); num4 - pipe length (m)
        num5 = num3 * 1e-3
        if num1 < 2300:
            sherwood_num = 0.023 * (num1**0.83) * (num2**0.33)
        else:
            sherwood_num = 3.65 + (
                (0.0668 * (num5 / num4) * num1 * num2)
                / (1 + 0.04 * ((num5 / num4) * num1 * num2) ** (2 / 3))
            )
        return sherwood_num

    # Defining Mass transfer coefficient for chlorine
    def mass_transfer_coefficient_cl(num1, num2, num3):
        # num1 - Sherwood number; num2 - molecular diffusivity of bulk species (sq.m/s); num3 - pipe diameter (mm)
        num4 = num3 * 1e-3
        kf_val_cl = num1 * (num2 / num4)
        return kf_val_cl

    # Defining Mass transfer coefficient for arsenic
    def mass_transfer_coefficient_ars(num1, num2, num3, num4):
        # num1 - molecular diffusivity of arsenic (sq.m/s); num2 - pipe diamter (mm); num3 - pipe flow velocity (m/s)
        # num4 - kinematic viscosity of water (sq.m/s)
        num5 = num2 * 1e-3
        if num5 == 0:
            kf_val_ars = 1
        else:
            kf_val_ars = 0.026 * (num1 / num5) * ((num5 * num3 / num4) ** 0.8) * ((num4 / num1) ** 0.333)
        return kf_val_ars

    # Defining Hydrauic mean radius
    def hydraulic_mean_radius(num1):
        # num1 - pipe diameter (mm)
        num2 = num1 * 1e-3
        rh_value = num2 / 4
        return rh_value

    # Defining Area of cross section
    def area_per_unit_vol(num1):
        # num1 - pipe diamter (mm)
        num2 = num1 * 1e-3
        area_val = 4 / (1e3 * num2)
        return area_val

    # Defining variables of the MSRT module
    def variables(num1, num2):
        # num1 - number of iterations; num2 - number of variables
        variable_mat = np.zeros((num1, num2))
        # Temperature (degree Celsius)
        temperature_mean = 25
        temperature_var = 0.5
        # Rate constant (chlorine - TOC reaction) (L/mg-C/s)
        kbNC_lower = 2.19e4
        kbNC_upper = 3.81e4
        kbNC_mean = 3e4
        # Rate constant (chlorine wall reaction) (m/s)
        kwC_lower = 1.04e-7
        kwC_upper = 1.43e-5
        kwC_mean = 1.22e-6
        # Reaction yield constant (chlorine - TOC reaction) (mg-C/ mg-Cl)
        YN_upper = 0.15
        YN_lower = 2.50
        YN_mean = 0.61
        # Adsorbance rate constant (for arsenic) (L/mg/s)
        k_ads = 6.67e-5
        # Equilibrium constant (for arsenic) (mg/L)
        k_eq = 0.054
        # Maximum adsorbance density (for As(V)) (mg/sq.m)
        S_max = 500
        # Rate constant (chlorine - As(III) reaction) (L/mg/s)
        kbCAs = 3.64
        # Reaction yield constant (chlorine - As(III) reaction) (mg-Cl/ mg-As(III))
        YC = 0.96
        # Molecular diffusivity of chlorine (sq.m/s)
        Dm_chlorine = 12.5e-10
        # Molecular diffusivity of TOC (sq.m/s)
        Dm_toc_lower = 7.8e-10
        Dm_toc_upper = 11.5e-10
        Dm_toc_mean = 9.5e-10
        # Molecular diffusivity of arsenic (sq.m/s)
        Dm_arsenic = 7.5e-10
        # Molecular diffusivity of THMs (sq.m/s)
        dens_water = 997
        # Kinematic viscosity of water (sq.m/s)
        nu_water = 9.31e-7
        if num1 == 1:
            variable_mat[num1 - 1][0] = temperature_mean
            variable_mat[num1 - 1][1] = kbNC_mean * math.exp(-6050 / (temperature_mean + 273))
            variable_mat[num1 - 1][2] = kwC_mean
            variable_mat[num1 - 1][3] = YN_mean
            variable_mat[num1 - 1][4] = k_ads
            variable_mat[num1 - 1][5] = k_eq
            variable_mat[num1 - 1][6] = S_max
            variable_mat[num1 - 1][7] = kbCAs
            variable_mat[num1 - 1][8] = YC
            variable_mat[num1 - 1][9] = Dm_chlorine
            variable_mat[num1 - 1][10] = Dm_toc_mean
            variable_mat[num1 - 1][11] = Dm_arsenic
            variable_mat[num1 - 1][12] = dens_water
            variable_mat[num1 - 1][13] = nu_water
        else:
            for x in range(num1):
                variable_mat[x][0] = (1 - temperature_var) * temperature_mean + (
                    2 * temperature_var * temperature_mean
                ) * random.uniform(0, 1)
                variable_mat[x][1] = random.uniform(kbNC_lower, kbNC_upper) * math.exp(
                    -6050 / ((variable_mat[x][0]) + 273)
                )
                variable_mat[x][2] = random.uniform(kwC_lower, kwC_upper)
                variable_mat[x][3] = random.uniform(YN_lower, YN_upper)
                variable_mat[x][4] = k_ads
                variable_mat[x][5] = k_eq
                variable_mat[x][6] = S_max
                variable_mat[x][7] = kbCAs
                variable_mat[x][8] = YC
                variable_mat[x][9] = Dm_chlorine
                variable_mat[x][10] = random.uniform(Dm_toc_lower, Dm_toc_upper)
                variable_mat[x][11] = Dm_arsenic
                variable_mat[x][12] = dens_water
                variable_mat[x][13] = nu_water
        return variable_mat

    # Defining pipe reactions for the MSRT model selected
    def pipe_reaction(num1, num2, num3, num4, num5, num6, num7, arr1, arr2):
        # num1 - water quality time step;num2 - pipe number; num3- grid number;
        # num4 - pipe flow velocity (m/s); num5 - pipe diameter (mm); num6 - pipe length; num7 - width of link segment (m)
        # arr1 - matrix of variables; arr2 = array of pipe concentration
        kbNC = arr1[1]
        kwC = arr1[2]
        YN = arr1[3]
        k_ads = arr1[4]
        k_eq = arr1[5]
        S_max = arr1[6]
        kbCAs = arr1[7]
        YC = arr1[8]
        Dm_chlorine = arr1[9]
        Dm_arsenic = arr1[11]
        nu_water = arr1[13]

        KbNC = kbNC * arr2[4][num3][num2]
        KbCAs = kbCAs * arr2[3][num3][num2]
        Re = module.Reynolds_number(num4, num5, nu_water)
        Sc_chlorine = module.Schmidt_number(nu_water, Dm_chlorine)
        Sh_chlorine = module.Sherwood_number(Re, Sc_chlorine, num5, num6)
        kfC = module.mass_transfer_coefficient_cl(Sh_chlorine, Dm_chlorine, num5)
        rh = module.hydraulic_mean_radius(num5)
        KwC = (kwC * kfC) / ((kwC + kfC) * rh)
        KfAs = module.mass_transfer_coefficient_ars(Dm_arsenic, num2, num4, nu_water)
        Sorb = (arr2[1][num3][num2] * (S_max - arr2[5][num3][num2]) - k_eq * arr2[5][num3][num2]) / (
            (1 / k_ads) + ((1 / KfAs) * (S_max - arr2[5][num3][num2]))
        )
        Av = module.area_per_unit_vol(num5)

        # Reactions within pipe
        delta_chlorine_toc_reac_pipe = module.first_order_reaction(KbNC, arr2[3][num3][num2], num1)
        delta_chlorine_wall_reac_pipe = module.first_order_reaction(KwC, arr2[3][num3][num2], num1)
        delta_toc_chlorine_reac_pipe = YN * delta_chlorine_toc_reac_pipe
        if module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1) > arr2[0][num3][num2]:
            delta_As3_chlorine_reac_pipe = arr2[0][num3][num2]
        else:
            delta_As3_chlorine_reac_pipe = module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1)
        delta_chlorine_As3_reac_pipe = YC * delta_chlorine_toc_reac_pipe
        if module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1) > arr2[0][num3][num2]:
            delta_As5_As3_reac_pipe = arr2[0][num3][num2]
        else:
            delta_As5_As3_reac_pipe = module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1)
        # delta_As5_As3_reac_pipe = 0
        delta_As5_bulk_reac_pipe = Av * Sorb
        delta_As5_wall_reac_pipe = Sorb

        net_delta_chlorine_reac = (
            -delta_chlorine_toc_reac_pipe - delta_chlorine_wall_reac_pipe - delta_chlorine_As3_reac_pipe
        )
        net_delta_toc_reac = -delta_toc_chlorine_reac_pipe
        net_delta_As3_reac = -delta_As3_chlorine_reac_pipe
        net_delta_As5_reac_bulk = delta_As5_As3_reac_pipe - delta_As5_bulk_reac_pipe
        net_delta_As5_reac_wall = delta_As5_wall_reac_pipe
        net_delta_As_reac = net_delta_As3_reac + net_delta_As5_reac_bulk

        delta_mat = [
            net_delta_As3_reac,
            net_delta_As5_reac_bulk,
            net_delta_As_reac,
            net_delta_chlorine_reac,
            net_delta_toc_reac,
            net_delta_As5_reac_wall,
        ]
        return delta_mat

    # Defining tank reactions for the MSRT model selected
    def tank_reaction(num1, num2, num3, num4, num5, arr1, arr2, arr3):
        # num1 - water quality time step; num2 - water quality step, num3 - tank number;
        # num4 - tank volume in the previous time step; num5 - tank volume in the present time step;
        # arr1 - matrix of variables; arr2 = initial water quality condition array; arr3 - array of tank concentration
        kbNC = arr1[1]
        YN = arr1[3]
        kbCAs = arr1[7]
        YC = arr1[8]

        if num2 == 1:
            tank_As3_conc = arr2[num3][0]
            tank_chlorine_conc = arr2[num3][3]
            tank_toc_conc = arr2[num3][4]
        else:
            tank_As3_conc = arr3[0][num2 - 1][num3]
            tank_chlorine_conc = arr3[3][num2 - 1][num3]
            tank_toc_conc = arr3[4][num2 - 1][num3]

        KbNC = kbNC * tank_toc_conc
        KbCAs = kbCAs * tank_chlorine_conc
        # Reactions within tank
        delta_chlorine_toc_reac_tank = (num4 / num5) * module.first_order_reaction(
            KbNC, tank_chlorine_conc, num1
        )
        delta_toc_chlorine_reac_tank = YN * delta_chlorine_toc_reac_tank
        if (num4 / num5) * module.first_order_reaction(KbCAs, tank_As3_conc, num1) > tank_As3_conc:
            delta_As3_chlorine_reac_tank = tank_As3_conc
        else:
            delta_As3_chlorine_reac_tank = (num4 / num5) * module.first_order_reaction(
                KbCAs, tank_As3_conc, num1
            )
        delta_chlorine_As3_reac_tank = YC * delta_As3_chlorine_reac_tank

        net_delta_chlorine_reac = -delta_chlorine_toc_reac_tank - delta_chlorine_As3_reac_tank
        net_delta_toc_reac = -delta_toc_chlorine_reac_tank
        net_delta_As3_reac = -delta_As3_chlorine_reac_tank
        net_delta_As5_reac = delta_As3_chlorine_reac_tank
        net_delta_As_reac = 0

        delta_mat = [
            net_delta_As3_reac,
            net_delta_As5_reac,
            net_delta_As_reac,
            net_delta_chlorine_reac,
            net_delta_toc_reac,
        ]
        return delta_mat

    # Defining source quality at the reservoir(s)
    def reservoir_quality(d, num1, arr1, str1, num2):
        # num1 - number of iterations; arr1 - source water quality input
        # str1 - input value for pattern; num2 - percentage variation in the random pattern
        num_reservoirs = module.network(d)[2]
        num_bulk_parameters = module.species()[1]
        if len(arr1) == num_reservoirs:
            if len(arr1[0]) == num_bulk_parameters:
                print("Reservoir quality updated.")
            else:
                print("Reservoir quality input error.")
                exit()
        reservoir_quality = np.zeros((num_reservoirs, num1, num_bulk_parameters))
        # Input
        # 'none' - constant values; 'rand' - randomly varying values
        input = str1
        rand_vary = num2  # percentage variation
        if input == "none":
            for x in range(num_reservoirs):
                reservoir_quality[x] = arr1[x]
        elif input == "rand":
            if num1 == 1:
                mat_min = arr1
                mat_max = arr1
            else:
                mat_min = np.multiply(arr1, (1 - rand_vary))
                mat_max = np.multiply(arr1, (1 + rand_vary))
            for x in range(num_reservoirs):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < num1:
                        reservoir_quality[x][z][y] = random.uniform(mat_min[x][y], mat_max[x][y])
                        z += 1
        return reservoir_quality

    # Defining source quality pattern for the reservoir(s)
    def reservoir_pattern(d, num1, str1, num2, arr1, arr2, arr3):
        # num1 - base time in days # str1 - input value for pattern; num2 - percentage variation in the random pattern
        # arr1 - reservoir injection start time steps; arr2 - reservoir injection stop time steps
        # arr3 - reservoir injection input value
        num_reservoirs = module.network(d)[2]
        num_bulk_parameters = module.species()[1]
        h_time = d.getTimeHydraulicStep()
        pattern_steps = int(num1 * 24 * 3600 / h_time)
        pattern_mat = np.zeros((num_reservoirs, pattern_steps, num_bulk_parameters))
        # Input
        # 'none' - constant pattern; 'rand' - random variations; 'specific - specify pattern
        input = str1
        rand_vary = num2  # percentage variation
        if input == "none":
            pattern_mat = np.add(pattern_mat, 1)
        elif input == "rand":
            for x in range(num_reservoirs):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < pattern_steps:
                        pattern_mat[x][z][y] = random.uniform(1 - rand_vary, 1 + rand_vary)
                        z += 1
        elif input == "specific":
            start_step_mat = arr1
            end_step_mat = arr2
            val_input = arr3
            if len(start_step_mat) == num_reservoirs and len(end_step_mat) == num_reservoirs:
                if len(start_step_mat[0]) <= pattern_steps and len(end_step_mat[0]) <= pattern_steps:
                    for x in range(num_reservoirs):
                        for y in range(len(start_step_mat[x])):
                            pattern_mat[x][start_step_mat[x][y] : end_step_mat[x][y]] = val_input[x][y]
            else:
                exit()
        return pattern_mat

    # Defining quality at the injection node(s)
    def injection_quality(num1, arr1, arr2, str1, num2):
        # num1 - number of iterations; arr1 - matrix of injection nodes indices; arr2 - matrix of injection nodes quality
        # str1 - input value for pattern; num2 - percentage variation in the random pattern
        num_injection_nodes = len(arr1)
        num_bulk_parameters = module.species()[1]
        if len(arr2) == num_injection_nodes:
            if len(arr2[0]) == num_bulk_parameters:
                print("Reservoir quality updated.")
            else:
                print("Injection node quality input error.")
                exit()
        injection_quality = np.zeros((num_injection_nodes, num1, num_bulk_parameters))
        print("Injection nodes quality updated.")
        # Input
        # 'none' - constant values; 'rand' - randomly varying values
        input = str1
        rand_vary = num2  # percentage variation
        if input == "none":
            for x in range(num_injection_nodes):
                injection_quality[x] = arr2[x]
        elif input == "rand":
            if num1 == 1:
                mat_min = arr2
                mat_max = arr2
            else:
                mat_min = np.multiply(arr2, (1 - rand_vary))
                mat_max = np.multiply(arr2, (1 + rand_vary))
            for x in range(num_injection_nodes):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < num1:
                        injection_quality[x][z][y] = random.uniform(mat_min[x][y], mat_max[x][y])
                        z += 1
        return injection_quality

    # Defining injection pattern for the injection node(s)
    def injection_pattern(d, num1, arr1, str1, num2, arr2, arr3, arr4):
        # num1 - base time in days; arr1 - matrix of injection nodes indices
        # str1 - input value for pattern; num2 - percentage variation in the random pattern
        # arr2 - injection node injection start time steps; arr3 - injection node injection stop time steps
        # arr4 - injection node injection input value
        num_injection_nodes = len(arr1)
        num_bulk_parameters = module.species()[1]
        h_time = d.getTimeHydraulicStep()
        pattern_steps = int(num1 * 24 * 3600 / h_time)
        inj_pattern_mat = np.zeros((num_injection_nodes, pattern_steps, num_bulk_parameters))
        # Input
        # 'none' - constant pattern; 'rand' - random variations; 'specific - specify pattern
        input = str1
        rand_vary = num2  # percentage variation
        if input == "none":
            inj_pattern_mat = np.add(inj_pattern_mat, 1)
        elif input == "rand":
            for x in range(num_injection_nodes):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < pattern_steps:
                        inj_pattern_mat[x][z][y] = random.uniform(1 - rand_vary, 1 + rand_vary)
                        z += 1
        elif input == "specific":
            start_step_mat = arr2
            end_step_mat = arr3
            val_input = arr4
            if len(start_step_mat) == num_injection_nodes and len(end_step_mat) == num_injection_nodes:
                if len(start_step_mat[0]) <= pattern_steps and len(end_step_mat[0]) <= pattern_steps:
                    for x in range(num_injection_nodes):
                        for y in range(len(start_step_mat[x])):
                            inj_pattern_mat[x][start_step_mat[x][y] : end_step_mat[x][y]] = val_input[x][y]
            else:
                exit()
        return inj_pattern_mat
