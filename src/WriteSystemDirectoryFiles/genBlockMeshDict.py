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


from __future__ import division
import numpy


class geometry:
	def __init__(self, parameters):
		self.Diam=parameters['Diam']
		self.domLenght=30*self.Diam
		self.domThick=parameters['thickness']
		self.domHeight=20*self.Diam

	def getVertex(self):
		#9 points on the bottom plane:
		pbottom=[[0,0,0],   #p0
			[self.domLenght/2,0,0],  #p1
			[self.domLenght,0,0],  #p2
			[0,self.domHeight/2,0],  #p3
			[self.domLenght/2,self.domHeight/2,0],  #p4
			[self.domLenght,self.domHeight/2,0], #p5
			[0,self.domHeight,0],#p6
			[self.domLenght/2,self.domHeight,0],  #p7
			[self.domLenght,self.domHeight,0]]   #p8
		#9 points in the middle plane
		pmid=[[0,0,self.domThick/2],  #p9
			[self.domLenght/2,0,self.domThick/2],  #p10
			[self.domLenght,0,self.domThick/2], #p11
			[0,self.domHeight/2,self.domThick/2], #p12
			[self.domLenght/2,self.domHeight/2,self.domThick/2], #p13
			[self.domLenght,self.domHeight/2,self.domThick/2],  #p14
			[0,self.domHeight,self.domThick/2],  #p15
			[self.domLenght/2,self.domHeight,self.domThick/2], #p16
			[self.domLenght,self.domHeight,self.domThick/2]]   #p17
		#9 points on the top plane:
		ptop=[[0,0,self.domThick],  #p18
			[self.domLenght/2,0,self.domThick],  #p19
			[self.domLenght,0,self.domThick],  #p20
			[0,self.domHeight/2,self.domThick],  #p21
			[self.domLenght/2,self.domHeight/2,self.domThick], #p22
			[self.domLenght,self.domHeight/2,self.domThick],  #p23
			[0,self.domHeight,self.domThick],  #p24
			[self.domLenght/2,self.domHeight,self.domThick], #p25
			[self.domLenght,self.domHeight,self.domThick]] #26
		pnts = numpy.vstack([pbottom,pmid])
		points = numpy.vstack([pnts,ptop])
		return points

	def getBlock(self):
		blocks =[[0, 1, 4, 3, 9, 10, 13, 12],
				[3, 4, 7, 6, 12, 13, 16, 15],
				[1, 2, 5, 4, 10, 11, 14, 13],
				[4, 5, 8, 7, 13, 14, 17, 16],
				[9, 10, 13, 12, 18, 19, 22, 21],
				[12, 13, 16, 15, 21, 22, 25, 24],
				[10, 11, 14, 13, 19, 20, 23, 22],
				[13, 14, 17, 16, 22, 23, 26, 25]]
		return blocks


class boundaryFace:
	def __init__(self, bcName, bcType):
		self.bcName = bcName
		self.bcType = bcType
		
	def getFaces(self, side):
		if side == 'east':
			face = [
				[6, 3, 12, 15],
				[3, 0, 9, 12],
				[15, 12, 21, 24],
				[12, 9, 18, 21]]
		elif side == 'back':
			face = [
	 			[6, 15, 16, 7],
	 			[7, 16, 17, 8],
	 			[15, 24, 25, 16],
	 			[16, 25, 26, 17]]
		elif side == 'front':
			face = [
	 			[2, 11, 10, 1],
	 			[1, 10, 9, 0],
	 			[11, 20, 19, 10],
	 			[10, 19, 18, 9]]
		elif side == 'west':
			face = [
	 			[8, 17, 14, 5],
	 			[5, 14, 11, 2],
	 			[17, 26, 23, 14],
	 			[14, 23, 20, 11]]
		elif side == 'top':
			face = [
	 			[24, 21, 22, 25],
	 			[21, 18, 19, 22],
	 			[25, 22, 23, 26],
	 			[22, 19, 20, 23]]
		elif side == 'bottom':
			face = [
	 			[6, 3, 4, 7],
	 			[3, 0, 1, 4],
	 			[7, 4, 5, 8],
	 			[4, 1, 2, 5]]
		return face

	def getBCName(self):
		return self.bcName

	def getBCType(self):
		return self.bcType


class genBlockMeshDictFile:
	def __init__(self, parameters, defBCname, defBCtype, defBCside):
		Diam=parameters['Diam']
		self.parameters = parameters
		self.defBCname = defBCname
		self.defBCtype = defBCtype
		self.defBCside = defBCside
		self.nBlocks = 8
		self.xCells = parameters['xCells']
		self.yCells = parameters['yCells']
		self.zCells = parameters['zCells']
		self.xGrading = parameters['xGrading']
		self.yGrading = parameters['yGrading']
		self.zGrading = parameters['zGrading']
		self.xGrdVec=[self.xGrading,self.xGrading,1/self.xGrading,1/self.xGrading,self.xGrading,self.xGrading,1/self.xGrading,1/self.xGrading]
		self.yGrdVec=[self.yGrading,1/self.yGrading,self.yGrading,1/self.yGrading,self.yGrading,1/self.yGrading,self.yGrading,1/self.yGrading]
		self.zGrdVec=[self.zGrading,self.zGrading,self.zGrading,self.zGrading,1/self.zGrading,1/self.zGrading,1/self.zGrading,1/self.zGrading]
		self.points = geometry(parameters).getVertex()
		self.prows = self.points.shape[0]
		self.Blocks = geometry(parameters).getBlock()
		self.boundaryConditions = {
			self.defBCside[0]   : boundaryFace(self.defBCname[0] , self.defBCtype[0]),
			self.defBCside[1]   : boundaryFace(self.defBCname[1] , self.defBCtype[1]),
			self.defBCside[2]   : boundaryFace(self.defBCname[2] , self.defBCtype[2]),
			self.defBCside[3]   : boundaryFace(self.defBCname[3] , self.defBCtype[3]),
			self.defBCside[4]   : boundaryFace(self.defBCname[4] , self.defBCtype[4]),
			self.defBCside[5]   : boundaryFace(self.defBCname[5] , self.defBCtype[5]),
				}

	def writeBlockFile(self):
		blockMeshDictFile = open("blockMeshDict", "w")
		blockMeshDictFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		blockMeshDictFile.write("\n| ==========                |                                           |")
		blockMeshDictFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		blockMeshDictFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		blockMeshDictFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		blockMeshDictFile.write("\n|    \\\\/     M anipulation  |                                           |")
		blockMeshDictFile.write("\n\\*---------------------------------------------------------------------*/")
		blockMeshDictFile.write("\nFoamFile")
		blockMeshDictFile.write("\n{")
		blockMeshDictFile.write("\n	version		2.0;")
		blockMeshDictFile.write("\n	format		ascii;")
		blockMeshDictFile.write("\n	class		dictionary;")
		blockMeshDictFile.write("\n	location	\"system\";")
		blockMeshDictFile.write("\n	object		blockMeshDict;")
		blockMeshDictFile.write("\n}")
		blockMeshDictFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		blockMeshDictFile.write("\n\nscale   1;")
		blockMeshDictFile.write("\n\nvertices")
		blockMeshDictFile.write("\n(")
		for p in range(0,self.prows):
			blockMeshDictFile.write("\n   (" + str(self.points[p][0]) + " " + str(self.points[p][1]) + " " + str(self.points[p][2]) + ")")
		blockMeshDictFile.write("\n);")
		blockMeshDictFile.write("\n\nblocks")
		blockMeshDictFile.write("\n(")
		for n in range(0,self.nBlocks):
			blockMeshDictFile.write("\n    hex (" + str(self.Blocks[n][0]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][1]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][2]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][3]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][4]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][5]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][6]))
			blockMeshDictFile.write(" " + str(self.Blocks[n][7]) + ")")
			blockMeshDictFile.write(" (" + str(int(self.xCells/2))+ " " + str(int(self.yCells/2))+ " " + str(int(self.zCells/2)) + ")" )
			blockMeshDictFile.write(" simpleGrading (" + str(self.xGrdVec[n])+ " " +  str(self.yGrdVec[n])+ " " +  str(self.zGrdVec[n]) + ")")
		blockMeshDictFile.write("\n);")
		blockMeshDictFile.write("\n\nedges")
		blockMeshDictFile.write("\n(")
		blockMeshDictFile.write("\n);")
		blockMeshDictFile.write("\n\nboundary")
		blockMeshDictFile.write("\n(")
		i=0
		for bc in self.boundaryConditions:
			side = list(self.boundaryConditions)#list(self.boundaryConditions.keys())
			faces = self.boundaryConditions[bc].getFaces(side[i])
			face1 = "(" + str(faces[0][0])
			face1 += " " + str(faces[0][1])
			face1 += " " + str(faces[0][2])
			face1 += " " + str(faces[0][3]) + ")"
			face2 = "(" + str(faces[1][0])
			face2 += " " + str(faces[1][1])
			face2 += " " + str(faces[1][2])
			face2 += " " + str(faces[1][3]) + ")"
			face3 = "(" + str(faces[2][0])
			face3 += " " + str(faces[2][1])
			face3 += " " + str(faces[2][2])
			face3 += " " + str(faces[2][3]) + ")"
			face4 = "(" + str(faces[3][0])
			face4 += " " + str(faces[3][1])
			face4 += " " + str(faces[3][2])
			face4 += " " + str(faces[3][3]) + ")"
			boundary = self.boundaryConditions[bc].getBCName()
			if self.boundaryConditions[bc].getBCType() == 'cyclic':
				if boundary == 'topWall':
					boundary = 'bottomWall'
				elif boundary == 'bottomWall':
					boundary = 'topWall'
			blockMeshDictFile.write("\n	" + boundary)
			blockMeshDictFile.write("\n	{")
			blockMeshDictFile.write("\n		type " + self.boundaryConditions[bc].getBCType()+";") 
			if self.boundaryConditions[bc].getBCType() == 'cyclic':
				blockMeshDictFile.write("\n		neighbourPatch  " + self.boundaryConditions[bc].getBCName()+";")
			blockMeshDictFile.write("\n		faces")
			blockMeshDictFile.write("\n		(")
			blockMeshDictFile.write("\n			" + face1)
			blockMeshDictFile.write("\n			" + face2)
			blockMeshDictFile.write("\n			" + face3)
			blockMeshDictFile.write("\n			" + face4)
			blockMeshDictFile.write("\n		);")
			blockMeshDictFile.write("\n	}")
			blockMeshDictFile.write("\n")
			i=i+1
		blockMeshDictFile.write("\n);")
		blockMeshDictFile.write("\n\n// ******************************************************************* //")

	def writeExtrudeMeshDict(self):
		extrudeMeshDictFile = open("extrudeMeshDict", "w")
		extrudeMeshDictFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		extrudeMeshDictFile.write("\n| ==========                |                                           |")
		extrudeMeshDictFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		extrudeMeshDictFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		extrudeMeshDictFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		extrudeMeshDictFile.write("\n|    \\\\/     M anipulation  |                                           |")
		extrudeMeshDictFile.write("\n\\*---------------------------------------------------------------------*/")
		extrudeMeshDictFile.write("\nFoamFile")
		extrudeMeshDictFile.write("\n{")
		extrudeMeshDictFile.write("\n	version		2.0;")
		extrudeMeshDictFile.write("\n	format		ascii;")
		extrudeMeshDictFile.write("\n	class		dictionary;")
		extrudeMeshDictFile.write("\n	location	\"system\";")
		extrudeMeshDictFile.write("\n	object		extrudeMeshDict;")
		extrudeMeshDictFile.write("\n}")
		extrudeMeshDictFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		extrudeMeshDictFile.write("\n\nconstructFrom		patch;")
		extrudeMeshDictFile.write('\n\nsourceCase		"../' + str(self.parameters['folderName']) + '";')
		extrudeMeshDictFile.write("\n\nsourcePatches		(" + str(self.defBCname[3]) +");")
		extrudeMeshDictFile.write("\n\nexposedPatchName	" + str(self.defBCname[2]) +";")
		extrudeMeshDictFile.write("\n\nflipNormals		false;")
		extrudeMeshDictFile.write("\n\nextrudeModel		linearNormal;")
		extrudeMeshDictFile.write("\n\nnLayers			1;")
		extrudeMeshDictFile.write("\n\nexpansionRation		1.0;")
		extrudeMeshDictFile.write("\n\nlinearNormalCoeffs")
		extrudeMeshDictFile.write("\n{")
		extrudeMeshDictFile.write("\n	thickness	0.5;")
		extrudeMeshDictFile.write("\n}")
		extrudeMeshDictFile.write("\n\nmergeFaces		false;")
		extrudeMeshDictFile.write("\n\nmergeTol		0;")
		extrudeMeshDictFile.write("\n\n// ******************************************************************* //")