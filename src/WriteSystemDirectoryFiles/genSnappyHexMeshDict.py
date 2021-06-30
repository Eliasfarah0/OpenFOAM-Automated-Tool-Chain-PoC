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
import math


class meshParam:
	def __init__(self,parameters, geometry, thick):
		self.parameters = parameters
		self.Diam = self.parameters['Diam']
		self.geometry = geometry
		self.flowType = self.parameters['flowType']
		self.physModel = self.parameters['physModel']
		self.thick = thick

	def getGeometry(self):
		return self.geometry

	def refinementBox(self):
		P10 = [10*self.Diam-1*self.Diam , 10*self.Diam-1*self.Diam, 0]
		P11 = [10*self.Diam+8*self.Diam , 10*self.Diam+1*self.Diam, self.thick]
		P20 = [10*self.Diam-5*self.Diam , 10*self.Diam-3*self.Diam, 0]
		P21 = [10*self.Diam+16*self.Diam , 10*self.Diam+3*self.Diam, self.thick]
		return P10, P11, P20, P21

	def castellatedControl(self):
		cstParameters = {'maxLocalCells' : 1000000, 
						'maxGlobalCells' : 20000000,
						'minRefinementCells' : 100000,
						'maxLoadUnbalance' : 0.10,
						'nCellsBetweenLevels' : 8,
						'geomlevel' : [4, 4],
						'box1level' : [1e-15, 4],
						'box2level' : [1e-15, 2], 
						'levels' : [0.1, 4],
						'resolveFeatureAngle' : 30}
		return cstParameters

	def snapControl(self):
		snpParameters = { 'nSmoothPatch' : 10,
							 'tolerance' : 0.5,
							 'nSolveIter' : 20, 
							 'nRelaxIter' : 3,
							 'nFeatureSnapIter' : 20,
							 'implicitFeatureSnap' : 'false',
							 'explicitFeatureSnap' : 'true',
							 'multiRegionFeatureSnap' : 'false'}
		return snpParameters

	def addLayersControl(self, wallSpacing):
		if self.flowType == 'laminar':
				#wallSpacing = 0.002 #0.004 for 3d heavy mesh
				nSurfaceLayers = 18 #12 for 3d heavy mesh
				expansionRatio = 1.05
		if self.flowType == 'RAS':
			expansionRatio = 1.05
			targetFinalThickness = 0.12
			finalLayerThickness = 0
			layerCounter = 0
			while finalLayerThickness <=targetFinalThickness:
				finalLayerThickness=finalLayerThickness+((wallSpacing*2)*pow(expansionRatio, layerCounter))
				layerCounter = layerCounter + 1
			nSurfaceLayers = layerCounter	
		layerParameters = { 'relativeSizes' : 'false',
							 'nSurfaceLayers' : nSurfaceLayers,
							 'expansionRatio' : expansionRatio, 
							 #'finalLayerThickness' : finalLayerThickness,
							 'firstLayerThickness' : wallSpacing*2, 
							 'minThickness' : wallSpacing/3,
							 'nGrow' : 0,
							 'featureAngle' : 60,
							 'slipFeatureAngle' : 60,
							 'nRelaxIter' : 3,
							 'nSmoothSurfaceNormals' : 5,
							 'nSmoothNormals' : 5,
							 'nSmoothThickness' : 10,
							 'maxFaceThicknessRatio' : 0.5,
							 'maxThicknessToMedialRatio' : 0.3,
							 'minMedialAxisAngle' : 90,
							 'nBufferCellsNoExtrude' : 0,
							 'nLayerIter' : 50}
		return layerParameters

	def meshQuality(self):
		qualityParameters = {'nSmoothScale' : 5, 
							'errorReduction' : 0.75,
							'mergeTolerance' : 1e-6}
		return qualityParameters


class genSnappyHexMeshDictFile:
	def __init__(self, parameters, wallSpacing):
		self.parameters=parameters
		self.Diam=parameters['Diam']
		self.wallSpacing = wallSpacing 
		self.thick=parameters['thickness']
		self.p00=[10*self.Diam,10*self.Diam,0]
		self.p01=[10*self.Diam,10*self.Diam,self.thick]
		self.test = meshParam(self.parameters , "cylinder", self.thick)
		self.refbox = self.test.refinementBox()
		self.castellated = self.test.castellatedControl()
		self.snapped = self.test.snapControl()
		self.addLayers  = self.test.addLayersControl(wallSpacing)
		self.mshQuality = self.test.meshQuality()

	def writeSnappyFile(self):
		snappyHexMeshDictFile = open("snappyHexMeshDict", "w")
		snappyHexMeshDictFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		snappyHexMeshDictFile.write("\n| ==========                |                                           |")
		snappyHexMeshDictFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		snappyHexMeshDictFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		snappyHexMeshDictFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		snappyHexMeshDictFile.write("\n|    \\\\/     M anipulation  |                                           |")
		snappyHexMeshDictFile.write("\n\\*---------------------------------------------------------------------*/")
		snappyHexMeshDictFile.write("\nFoamFile")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write("\n	version		2.0;")
		snappyHexMeshDictFile.write("\n	format		ascii;")
		snappyHexMeshDictFile.write("\n	class		dictionary;")
		snappyHexMeshDictFile.write("\n	location	\"system\";")
		snappyHexMeshDictFile.write("\n	object		SnappyHexMeshDict;")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		snappyHexMeshDictFile.write("\n\ncastellatedMesh true;")
		snappyHexMeshDictFile.write("\nsnap true;")
		snappyHexMeshDictFile.write("\naddLayers true;")
		snappyHexMeshDictFile.write("\n\ngeometry")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write("\n	" + self.test.getGeometry())
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		type searchableCylinder;")
		snappyHexMeshDictFile.write("\n		point1 ("+ str(self.p00[0]) + " " + str(self.p00[1]) + " " + str(self.p00[2]) +");")
		snappyHexMeshDictFile.write("\n		point2 ("+ str(self.p01[0]) + " " + str(self.p01[1]) + " " + str(self.p01[2]) +");")
		snappyHexMeshDictFile.write("\n		radius " +str(self.Diam/2)+";")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	refinementBox1")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		type searchableBox;")
		snappyHexMeshDictFile.write("\n		min (" + str(self.refbox[0][0]) + " " + str(self.refbox[0][1]) + " " + str(self.refbox[0][2]) + ");")
		snappyHexMeshDictFile.write("\n		max (" + str(self.refbox[1][0]) + " " + str(self.refbox[1][1]) + " " + str(self.refbox[1][2]) + ");")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	refinementBox2")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		type searchableBox;")
		snappyHexMeshDictFile.write("\n		min (" + str(self.refbox[2][0]) + " " + str(self.refbox[2][1]) + " " + str(self.refbox[2][2]) + ");")
		snappyHexMeshDictFile.write("\n		max (" + str(self.refbox[3][0]) + " " + str(self.refbox[3][1]) + " " + str(self.refbox[3][2]) + ");")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n\ncastellatedMeshControls")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write("\n	maxLocalCells  " + str(self.castellated['maxLocalCells']) +";")
		snappyHexMeshDictFile.write("\n	maxGlobalCells  " + str(self.castellated['maxGlobalCells']) +";")
		snappyHexMeshDictFile.write("\n	minRefinementCells " + str(self.castellated['minRefinementCells']) +";")
		snappyHexMeshDictFile.write("\n	maxLoadUnbalance " + str(self.castellated['maxLoadUnbalance']) +";")
		snappyHexMeshDictFile.write("\n	nCellsBetweenLevels " + str(self.castellated['nCellsBetweenLevels']) +";")
		snappyHexMeshDictFile.write("\n	features")
		snappyHexMeshDictFile.write("\n	(")
		snappyHexMeshDictFile.write("\n	);")
		snappyHexMeshDictFile.write("\n	refinementSurfaces")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		cylinder")
		snappyHexMeshDictFile.write("\n		{")
		snappyHexMeshDictFile.write("\n			level  (" + str(self.castellated['geomlevel'][0]) + " " + str(self.castellated['geomlevel'][1]) +");")
		snappyHexMeshDictFile.write("\n			faceType boundary;")
		snappyHexMeshDictFile.write("\n			patchInfo")
		snappyHexMeshDictFile.write("\n			{")
		snappyHexMeshDictFile.write("\n				type wall;")
		snappyHexMeshDictFile.write("\n			}")
		snappyHexMeshDictFile.write("\n		}")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	cylinder")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		mode distance;")
		snappyHexMeshDictFile.write("\n		levels  ((" + str(self.castellated['levels'][0]) + " " + str(self.castellated['levels'][1]) +"));")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	resolveFeatureAngle " + str(self.castellated['resolveFeatureAngle']) + ";")
		snappyHexMeshDictFile.write("\n	refinementRegions")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write("\n		refinementBox1")
		snappyHexMeshDictFile.write("\n		{")
		snappyHexMeshDictFile.write("\n			mode inside;")
		snappyHexMeshDictFile.write("\n			levels ((" + str(self.castellated['box1level'][0]) + " " +str(self.castellated['box1level'][1]) + "));")
		snappyHexMeshDictFile.write("\n		}")
		snappyHexMeshDictFile.write("\n		refinementBox2")
		snappyHexMeshDictFile.write("\n		{")
		snappyHexMeshDictFile.write("\n			mode inside;")
		snappyHexMeshDictFile.write("\n			levels ((" + str(self.castellated['box2level'][0]) + " " +str(self.castellated['box2level'][1]) + "));")
		snappyHexMeshDictFile.write("\n		}")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	locationInMesh (" + str(self.Diam/2) + " " + str(self.Diam/2) + " " + str(self.Diam/4) + " );")
		snappyHexMeshDictFile.write("\n	allowFreeStandingZoneFaces true;")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n\nsnapControls")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write("\n	nSmoothPatch " + str(self.snapped['nSmoothPatch']) + ";")
		snappyHexMeshDictFile.write("\n	tolerance " + str(self.snapped['tolerance']) + ";")
		snappyHexMeshDictFile.write("\n	nSolveIter " + str(self.snapped['nSolveIter']) + ";")
		snappyHexMeshDictFile.write("\n	nRelaxIter " + str(self.snapped['nRelaxIter']) + ";")
		snappyHexMeshDictFile.write("\n	nFeatureSnapIter " + str(self.snapped['nFeatureSnapIter']) + ";")
		snappyHexMeshDictFile.write("\n	implicitFeatureSnap " + str(self.snapped['implicitFeatureSnap']) + ";")
		snappyHexMeshDictFile.write("\n	explicitFeatureSnap " + str(self.snapped['explicitFeatureSnap']) + ";")
		snappyHexMeshDictFile.write("\n	multiRegionFeatureSnap " + str(self.snapped['multiRegionFeatureSnap']) + ";")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n\naddLayersControls")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write("\n	relativeSizes " + str(self.addLayers['relativeSizes']) + ";")
		snappyHexMeshDictFile.write("\n	layers")
		snappyHexMeshDictFile.write("\n	{")
		snappyHexMeshDictFile.write('\n		"cylinder*.*"')
		snappyHexMeshDictFile.write("\n		{")
		snappyHexMeshDictFile.write("\n			nSurfaceLayers " + str(self.addLayers['nSurfaceLayers']) + ";")
		snappyHexMeshDictFile.write("\n		}")
		snappyHexMeshDictFile.write("\n	}")
		snappyHexMeshDictFile.write("\n	expansionRatio " + str(self.addLayers['expansionRatio']) + ";")
		#snappyHexMeshDictFile.write("\n	finalLayerThickness " + str(self.addLayers['finalLayerThickness']) + ";")
		snappyHexMeshDictFile.write("\n	firstLayerThickness " + str(self.addLayers['firstLayerThickness']) + ";")
		snappyHexMeshDictFile.write("\n	minThickness " + str(self.addLayers['minThickness']) + ";")
		snappyHexMeshDictFile.write("\n	nGrow " + str(self.addLayers['nGrow']) + ";")
		snappyHexMeshDictFile.write("\n	featureAngle " + str(self.addLayers['featureAngle']) + ";")
		snappyHexMeshDictFile.write("\n	slipFeatureAngle " + str(self.addLayers['slipFeatureAngle']) + ";")
		snappyHexMeshDictFile.write("\n	nRelaxIter " + str(self.addLayers['nRelaxIter']) + ";")
		snappyHexMeshDictFile.write("\n	nSmoothSurfaceNormals " + str(self.addLayers['nSmoothSurfaceNormals']) + ";")
		snappyHexMeshDictFile.write("\n	nSmoothNormals " + str(self.addLayers['nSmoothNormals']) + ";")
		snappyHexMeshDictFile.write("\n	nSmoothThickness " + str(self.addLayers['nSmoothThickness']) + ";")
		snappyHexMeshDictFile.write("\n	maxFaceThicknessRatio " + str(self.addLayers['maxFaceThicknessRatio']) + ";")
		snappyHexMeshDictFile.write("\n	maxThicknessToMedialRatio " + str(self.addLayers['maxThicknessToMedialRatio']) + ";")
		snappyHexMeshDictFile.write("\n	minMedialAxisAngle " + str(self.addLayers['minMedialAxisAngle']) + ";")
		snappyHexMeshDictFile.write("\n	nBufferCellsNoExtrude " + str(self.addLayers['nBufferCellsNoExtrude']) + ";")
		snappyHexMeshDictFile.write("\n	nLayerIter " + str(self.addLayers['nLayerIter']) + ";")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n\nmeshQualityControls")
		snappyHexMeshDictFile.write("\n{")
		snappyHexMeshDictFile.write('\n	#include "meshQualityDict"')
		snappyHexMeshDictFile.write("\n	nSmoothScale " + str(self.mshQuality['nSmoothScale']) + ";")
		snappyHexMeshDictFile.write("\n	errorReduction " + str(self.mshQuality['errorReduction']) + ";")
		snappyHexMeshDictFile.write("\n}")
		snappyHexMeshDictFile.write("\n\nwriteFlags")
		snappyHexMeshDictFile.write("\n(")
		snappyHexMeshDictFile.write('\n	scalarLevels')
		snappyHexMeshDictFile.write("\n	layerSets")
		snappyHexMeshDictFile.write("\n	layerFields")
		snappyHexMeshDictFile.write("\n);")
		snappyHexMeshDictFile.write("\n\nmergeTolerance " + str(self.mshQuality['mergeTolerance']) + ";")
		snappyHexMeshDictFile.write("\n\n// ******************************************************************* //")