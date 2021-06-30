FOLDER_NAME		= "cylinder_2D_steady_RAS_KWSST_Re_6e5"	# Case Directory Name
DIAMETER		= 1					# Cylinder Diameter
THICKNESS		= 1					# Cylinder Thickness in z-direction, "THICKNESS = 1" for 2D & "THICKNESS = 4" for 3D
VELOCITY		= 1					# Flow Velocity
REYNOLDS_NUMBER		= 600000				# Value of Re Number
DENSITY			= 1.225					# Flow Density
START_TIME		= 0					# Simulation Start Time
TIME_STEP		= 0.04					# Simulation Time Step, if "TIME_DERIVATIVE = "steady"" -> TIME_STEP = 1 by default (No need to fill for any value)
END_TIME		= 150					# Simulation End Time
WRITE_INTERVAL		= 50					# Controls the timing of write output to file per every WRITE_INTERVAL time steps
NUMBER_OF_PROCESSORS	= 1					# Number of Processors (CPU), "NUMBER_OF_PROCESSORS = 1" for Serial Run & "NUMBER_OF_PROCESSORS > 1" for Parallel Run
TOPOLOGY		= "2D"					# Geometrical Topology, "TOPOLOGY = 2D" for 2D Simulation & "TOPOLOGY = 3D" for 3D Simulation
TIME_DERIVATIVE		= "steady"				# Time Resolution, "TIME_DERIVATIVE = steady" for Steady-State Simulation & "TIME_DERIVATIVE = unsteady" for Transient Simulation
FLOW_TYPE		= "RAS"					# Flow Type, "FLOW_TYPE = laminar" for laminar flow & "FLOW_TYPE = RAS" for turbulent flow
TURBULENCE_MODEL	= "kOmegaSST"				# RANS Turbulence Models, "TURBULENCE_MODEL = SpalartAllmaras _or_ kEpsilon _or_ kOmega _or_ kOmegaSST"
PHYSICAL_MODEL		= "wallModeled"				# Near Wall Modelling, "PHYSICAL_MODEL = wallResolved" for y+ = 1 & "PHYSICAL_MODEL = wallModeled" for y+ >= 30 (i.e. using wall functions)