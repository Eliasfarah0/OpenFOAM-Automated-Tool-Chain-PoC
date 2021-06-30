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


import os, os.path, sys, string, shutil, glob, subprocess, math


class callSolver(object):
	def __init__(self, parameters):
		self.parameters = parameters

	def initialiseFlowField(self):
		print("\nInitialising the flow field...")
		argv = "potentialFoam" # -noFunctionObjects"
		subprocess.call(argv)

	def decomposingMeshSolver(self):
		print("\nOpenFOAM parallel simulation enabled, proceeding with decomposition of the mesh and fields...")
		args=["decomposePar"]
		subprocess.call(args)
		print("\nDecomposition finished, running now the Solver...") 
		argr = "mpirun -np " + str(self.parameters["procs"]) + " " + str(self.parameters["solver"]) + " -parallel"
		#mpirun -np 4 simpleFoam -parallel
		subprocess.call(argr, shell = True)

	def reconstructingMeshSolver(self):
		print("\nReconstructing the mesh and fields...")
		argv=["reconstructPar"]
		subprocess.call(argv)

	def nodecomposingMeshSolver(self):
		print("\nRunning the Solver...")
		args = [self.parameters["solver"]]
		subprocess.call(args)

	def startSolvingProcess(self):
		if self.parameters["timeDerivative"] == "steady" and self.parameters["flowType"] == "RAS": #self.parameters["startTime"] == 0:
			self.initialiseFlowField()
		if self.parameters["procs"] > 1:
			self.decomposingMeshSolver()
			self.reconstructingMeshSolver()
		else:
			self.nodecomposingMeshSolver() 
		print("\nSimulation completed.")