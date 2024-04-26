# EPyT-C - Fully independent multi-species reactive transport modelling extension for EPyT (EPANET-Python) toolkit

An open-source Python package for modeling water quality in water distribution systems.

## EPyT (EPANET-Python) toolkit

EPyT is an open-source software, initially developed by the KIOS Research and Innovation Center of Excellence, University of Cyprus, operating within the Python environment for providing a PYTHON programming interface for the latest version of EPANET ([Rossman et al., 2020](https://epanet22.readthedocs.io/_/downloads/en/latest/pdf/)). It calls EPANET as a shared object and employs an Object-Oriented approach for interfacing EPANET with PYTHON.

## Water quality modeling extensions of EPyT-C

Though EPyT can be employed for performing single-species water quality analysis, which comes within the scope of EPANET 2.2, it lacks multi-species reactive-transport modeling capability in its current form. In other words, EPyT can only analyze one water quality parameter at a time. Consequently, the water quality modeling compartment of EPyT needs to be improved to solve several real-world problems concerning water quality variations during delivery via WDS. A fully independent water quality modeling extension, EPyT-C, is developed in this direction. EPyT-C employs the hydraulic solver of EPANET 2.2 for performing hydraulic simulation, which the in-built water quality solver then utilizes for performing MSRT modeling.

### EPyT-C is now equipped with four MSRT modules.

| EPyT-C module                                         | Water quality parameters considered and their units                                                                                                                                                            | Processes considered within the pipe domain                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Chlorine decay and Trihalomethanes formation          | Bulk phase: (1) chlorine (mg/L); (2) total organic carbon, TOC (mg/L); and (3) trihalomethanes, THMs (ug/L).                                                                                                   | (1) chlorine - TOC reaction leading to chlorine decay, TOC degradation, and THMs formation; (2) mass-transfer of chlorine from bulk to wall phase; and (3) wall reactions of chlorine leading to its decay.                                                                                                                                                                                                              |
| Bacterial regrowth                                    | Bulk phase: (1) chlorine (mg/L); (2) recalcitrant dissolved organic carbon, RDOC (mg/L); (3) biodegradable DOC, BDOC (mg/L); (4) free living bacteria, FLB (CFU/L); and (5) free dead bacteria, FDB (cells/L). | (1) chlorine - RDOC reaction leading to chlorine decay and RDOC degradation; (2) chlorine - BDOC reaction leading to chlorine decay and BDOC degradation; (3) mass-transfer of chlorine from bulk to wall phase; and (4) wall reactions of chlorine leading to its decay; (5) bacterial growth and subsequent BDOC utilization; (6) bacterial mortality and FDB formation; and (7) FDB cell lysis and BDOC contribution. |
| Arsenite oxidation and arsenate attachment/detachment | Bulk phase: (1) aqueous arsenite (mg/L); (2) aqueous arsenate (mg/L); (3) aqueous arsenic (mg/L); (4) residual chlorine (mg/L); and (5) TOC (mg/L). Wall phase: (1) adsorbed arsenate (mg/m<sup>2</sup>).      | (1) chlorine - TOC reaction leading to chlorine decay, TOC degradation, and THMs formation; (2) mass-transfer of chlorine from bulk to wall phase; (3) wall reactions of chlorine leading to its decay; (4) chlorine – aqueous arsenite reaction leading to arsenite oxidation to arsenate and subsequent chlorine decay; (5) adsorption/ desorption of arsenate within the bulk-wall phase interface.                   |
| Perfluorooctanoic acid formation                      | Bulk phase: (1) chlorine (mg/L); (2) TOC (mg/L); (3) perfluoro octaneamido betaine, PFOAB (ng/L); (4) perfluoro octaneamido ammonium salt, PFOAAmS (ng/L); and perfluorooctanoic acid, PFOA (ng/L).            | (1) chlorine - TOC reaction leading to chlorine decay, TOC degradation, and THMs formation; (2) mass-transfer of chlorine from bulk to wall phase; (3) wall reactions of chlorine leading to its decay; (4) chlorine - PFOAB reaction leading to chlorine decay, PFOAB degradation, and PFOA formation; and (5) chlorine - PFOAAmS reaction leading to chlorine decay, PFOAAmS degradation, and PFOA formation.          |

Based on the module selected for WDS analysis, EPyT-C evolves governing (partial differential and ordinary differential) equations emulating the propagation and formation/ degradation of the corresponding water quality parameters within the distribution network realm. Once the governing equations (one-dimensional advective-reactive equations) are framed, the numerical method that involves the explicit method of characteristics and the fourth-order Runge-Kutta method, initially presented by ([Tzatchkov et al., 2002](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9496%282002%29128%3A5%28334%29)), is applied to derive numerical solutions - spatiotemporal distribution of complex water quality parameters in WDS.

## Flexibilities

EPyT-C offers the following flexibilities, making it a handy tool for research and industry:

1. Allows time-series variations in the input values for the water quality parameters at the sources (reservoirs and booster nodes).
2. Customize the random fluctuations in the input values for the water quality parameters at the sources.
3. Customize the perturbations in the reaction rate coefficient values.
4. Customize the outputs and export the data as Excel files or other formats.
5. Customize the numerical accuracy by altering the model parameters (time step, velocity tolerance, etc.).
6. Control the computational efficiency by adjusting the accuracy of the numerical solutions.

## Code instructions

The documentation can be found at http://epyt-c.readthedocs.io/ (in progress).

### Environment setup

- Create a new Conda environment as `epyt-c`
- Install the requirements from `requirements.txt`
- Install the package using `pip install .`

### Specifying the INP file (network data)

We provide two network INP fles (Net1 and Net3) in the Networks folder. The user can use any INP file. The INP file can be input to the script using the following code:

```
path_name = r"path\to\INP\file.inp"
epytc.network_name = os.path.normpath(path_name)
```

where `epytc` is an object of `epytc_class` class (please refer to `main_epytc.py`). The above code must be run after creating the `epytc_class` object. Please use the absoulte path.

### Sample python script

We provide a sample python script (`run_sample.py`) to demonstrate the functioning of EPyT-C. The default values for the parameters can be found in `default_values.yaml` under `epyt_c` and the associated `README.md` file provides an explanation of the parameters. To run the script with the default values for the parameters run `run_sample.py`. Please update the INP file path before running the script.

### Examples

We provide examples as Jupyter Notebooks. Please update the network INP file path to the network that you would like to use before running the notebooks. Make sure that the `epyt_c` package is installed in the environment that you are using to run the notebooks.

## Dependencies

- EPyT
- NumPy
- Pandas
- XlsxWriter
- Hydra

## Contact

**Gopinathan R Abhijith** - abhijith@iitk.ac.in

**Jaykrishnan G** - jaykrishnan.gp@gmail.com

**Avi Ostfeld** - ostfeld@technion.ac.il

## Credits

The **Smart Water Infrastructure Laboratory, Indian Institute of Technology Kanpur** and **Technion Israel Institute of Technology** jointly created this package.
