#########################################################################
#                                                                       #
#                C R A N F I E L D   U N I V E R S I T Y                #
#                          2 0 1 9  /  2 0 2 0                          #
#                                                                       #
#               MSc in Aerospace Computational Engineering              #
#                                                                       #
#                          Group Design Project                         #
#                                                                       #
#           Driver File for the OpenFoam Automated Tool Chain           #
#                      Flow Past Cylinder Test Case                     #
#                                                                       #
#-----------------------------------------------------------------------#
#                                                                       #
#   Main Contributors:                                                  #
#       Vadim Maltsev          (Email: V.Maltsev@cranfield.ac.uk)       #
#       Samali Liyanage        (Email: Samali.Liyanage@cranfield.ac.uk) #
#       Elias Farah            (Email: E.Farah@cranfield.ac.uk)         #
#   Supervisor:                                                         #
#       Dr. Tom-Robin Teschner (Email: Tom.Teschner@cranfield.ac.uk )   #
#                                                                       #
#########################################################################


from __future__             import division
import os, os.path, sys, string, shutil, glob, subprocess, math
from src.DriverFiles.directoriesDriver		import createDirectories
from src.DriverFiles.meshingDriver      	import callMeshing
from src.DriverFiles.solverDriver       	import callSolver
from src.DriverFiles.postProcessingDriver	import callPostProcessing
from src import User_Inputs_Parameters as UI_parameters


##########################
# USER INPUTS PARAMETERS #
##########################
parameters = {	"folderName"     : UI_parameters.FOLDER_NAME,
				"Diam"           : UI_parameters.DIAMETER,
				"thickness"      : UI_parameters.THICKNESS,
				"U"              : UI_parameters.VELOCITY,
				"Re"             : UI_parameters.REYNOLDS_NUMBER,
				"rho"            : UI_parameters.DENSITY,
				"startTime"      : UI_parameters.START_TIME,
				"deltaT"         : UI_parameters.TIME_STEP,
				"endTime"        : UI_parameters.END_TIME,
				"writeInterval"  : UI_parameters.WRITE_INTERVAL,
				"procs"          : UI_parameters.NUMBER_OF_PROCESSORS,
				"topology"       : UI_parameters.TOPOLOGY,
				"timeDerivative" : UI_parameters.TIME_DERIVATIVE,
				"flowType"       : UI_parameters.FLOW_TYPE,
				"turbModel"      : UI_parameters.TURBULENCE_MODEL,
				"physModel"      : UI_parameters.PHYSICAL_MODEL,
			}


##############################
# BOUNDARY CONDITIONS INPUTS #
##############################
# Enter the boundary conditions name and typology in the same order
defBCside = ["east" , "west"  , "top"    , "bottom"    , "front"    , "back"]
defBCname = ["inlet", "outlet", "topWall", "bottomWall", "frontWall", "backWall"]
defBCtype = ["patch", "patch" , "cyclic" , "cyclic"    , "symmetry" , "symmetry"]


#####################
# TURBULENCE INPUTS #
#####################
parameters["nu"] = parameters["U"] * parameters["Diam"] / parameters["Re"]
if parameters["flowType"] == "RAS":
	parameters["turbIntensity"] = 0.01
	parameters["Cmu"] = 0.09
	parameters["nuTilda"] = math.sqrt(1.5) * abs(parameters["U"]) * parameters["turbIntensity"] * parameters["Diam"]
	parameters["turbk"]  = 1.5 * pow((abs(parameters["U"]) * parameters["turbIntensity"]), 2) #For isotropic turbulence, the turbulent kinetic energy
	parameters["epsilon"] = pow(parameters["Cmu"], 0.75) * pow(parameters["turbk"], 1.5) / parameters["Diam"] #For isotropic turbulence, the turbulence dissipation rate
	parameters["omega"] = pow(parameters["Cmu"], -0.25) * pow(parameters["turbk"], 0.5) / parameters["Diam"]


##################
# MESHING INPUTS #
##################
if parameters["flowType"] == "RAS":
	if parameters["physModel"] == "wallModeled":
		parameters["yplus"]  = 30
	elif parameters["physModel"] == "wallResolved":
		parameters["yplus"]  = 1 # 5

#for Reynolds numbers between 10 and 100000 60x60 cells shoulb enough to ensure the layers addition
#for higher Reynolds and lower wallSpacing value a finer mesh 90x90 is suggested
if parameters["topology"] == "2D":
	parameters["xCells"] = 60
	parameters["yCells"] = 60
	parameters["zCells"] = 2
elif parameters["topology"] == "3D":
	parameters["xCells"] = 40
	parameters["yCells"] = 40
	parameters["zCells"] = 20

parameters["xGrading"] = 2
parameters["yGrading"] = 2
parameters["zGrading"] = 1


#################
# SOLVER INPUTS #
#################
if parameters["timeDerivative"] == "steady":
	parameters["solver"] = "simpleFoam" # simpleFoam (for steady   state simulation for both laminar and turbulent) 
elif parameters["timeDerivative"] == "unsteady":
	parameters["solver"] = "pimpleFoam" # pimpleFoam (for unsteady state simulation for both laminar and turbulent)
# SIMPLE ALGORITHM
parameters["consistent"] = "yes"	# yes or no


##########################
# POST PROCESSING INPUTS #
##########################
singleGraphs = [{"start":"(0 10 1.25)", "end":"(30 10 1.25)", "fields":"(U p)"}, {"start":"(0 15 1.25)", "end":"(30 15 1.25)", "fields":"(U p)"}]
cuttingPlanes = [{"planeName":"xPlane","point":"(15 0 1.25)", "normal":"(1 0 0)", "fields": "(U p)"}, {"planeName":"yPlane","point":"(0 10 1.25)", "normal":"(0 1 0)", "fields": "(U p)"}, {"planeName":"zPlane","point":"(15 10 1.5)", "normal":"(0 0 1)", "fields": "(U p)"}]


##################################################################################################################################
##################################################################################################################################


###############################
# Printing All The Parameters #
###############################
if parameters["flowType"] == "laminar":
	userParams = ["folderName", "Diam", "thickness", "U", "Re", "rho", "nu", "startTime", "deltaT", "endTime", "writeInterval", "procs", "topology", "timeDerivative", "flowType", "turbModel", "physModel"]
elif parameters["flowType"] == "RAS":
	userParams = ["folderName", "topology", "Diam", "thickness", "U", "Re", "rho", "startTime", "deltaT", "endTime", "writeInterval", "procs", "timeDerivative", "flowType", "turbModel", "physModel", "turbIntensity", "Cmu", "nu", "nuTilda", "turbk", "epsilon", "omega"]
print("\nThe chosen parameters are listed below:")
for i in userParams: print(str(i)+": "+str(parameters[i]))	
#print("\n".join("{}: {}".format(k, v) for k, v in parameters.items()))


##################################################
# Generate 0/, constant/ and system/ Directories #
##################################################
meshingObject = callMeshing(parameters)
directoriesObject = createDirectories(parameters, defBCname, defBCtype, defBCside, singleGraphs, cuttingPlanes)
if parameters["flowType"] == "RAS":
	wallSpacing = meshingObject.getFirstCellSpacing()
elif parameters["flowType"] == "laminar":
	wallSpacing = 0.001

print("\nGuessed first cells layer distance for the required yPlus: " +str(wallSpacing))
directoriesObject.startCreatingDirectories(wallSpacing, sgParams=len(singleGraphs), cpParams=len(cuttingPlanes))


###################
# Meshing Process #
###################
print("\nDo you want to create the mesh? (Type: Y or N)")
msh = input("(Y/N) << ").lower()

if msh in ["yes", "y"]:
	meshingObject.startMeshingProcess()
	directoriesObject.polyMeshFiles()
	if parameters["topology"] == '2D':
		meshingObject.generate2Dmesh()

if msh in ["no", "n"]:
	print("\nThe last mesh will be used in the run folder.")


###################
# Solving Process #
###################
print("\nStart the solver? (Type: Y or N)")
slvr = input("(Y/N) << ").lower()


if slvr in ["yes", "y"]:
	callSolver(parameters).startSolvingProcess()

if msh in ["no", "n"]:
	print("\nThe solution files will be used in the run folder.")


################
# Post Process #
################
postProcessObject = callPostProcessing(parameters)

print("\nDo you want to generate graphs for Lift and Drag? (Type: Y or N)")
ld_in = input("(Y/N) << ").lower()
if ld_in in ["yes", "y"]:
	postProcessObject.outputForceCoeffs()
	subprocess.call(["gnuplot", "-p", "lift.gp"])
	subprocess.call(["gnuplot", "-p", "drag.gp"])

print("\nDo you want to print the Strouhal Number? (Type: Y or N)")
strouhal_in = input("(Y/N) << ").lower()
if strouhal_in in ["yes", "y"]:
	#print("\nEnter time from which data is to be considered for Strouhal Number (Enter intger)")
	#time_strouhal = input("Time << ").lower()
	#if time_strouhal.isdigit():
	postProcessObject.strouhalNumberCalculation()
	subprocess.call(["gnuplot", "-p", "strouhal.gp"])

print("\nDo you want to generate the Single Graph? (Type: Y or N)")
sg_in = input("(Y/N) << ").lower()
while sg_in in ["yes", "y"]:
	if sg_in in ["yes", "y"]:
		print("\nEnter time from which data is to be considered for the graph (Enter intger)")
		time_sg = input("Time << ").lower()

		if len(singleGraphs)>1:
			print("\nEnter singleGraph for which you want data?")
			whichGraph_sg = input("Integer from 1 to "+str(len(singleGraphs))+"  << ")
		else:
			whichGraph_sg = None

		print("\nEnter component for which you want data?")
		component_sg = input("U or p << ")
		if set(component_sg).issubset(['U', 'p']) == False:
			component_sg = 'U'


		if component_sg == 'U':
			print("\nEnter axes for which you want data?")
			component_axes = input("i.e. xyz, xz, y etc. << ").lower()
			component_axes = list(component_axes)
			if set(component_axes).issubset(['x', 'y', 'z']) == False:
				component_axes = ['x', 'y', 'z']
		else:
			component_axes = ["x"]
		postProcessObject.outputSingleGraph(time_sg, whichGraph_sg, component_sg, component_axes)
		subprocess.call(["gnuplot", "-p", "singleGraph_"+component_sg+".gp"])
	print("\nDo you want to generate another Single Graph? (Type: Y or N)")
	sg_in = input("(Y/N) << ").lower()