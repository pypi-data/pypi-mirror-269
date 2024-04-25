from extractStructuresWithMC import extractStructuresMC
from boxcounting import boxCount
from percolationAnalysis import percolationAnalysis
import numpy as np
import math
import os
import array
from numba import jit

#---------------------------------------------------------------------#

# ---------Analysis of Multiscale Data from the Geosciences---------- #

# Author: Abhishek Harikrishnan
# Email: abhishek.harikrishnan@fu-berlin.de
# Last updated: 22-04-2024
# 
# Multilevel percolation analysis for obtaining simple structures, all
# of which exist at unique thresholds. Method has been described in the
# following preprint:

# Harikrishnan, Abhishek, et al. "Geometry and organization of coherent 
# structures in stably stratified atmospheric boundary layers." arXiv 
# preprint arXiv:2110.02253 (2021).

#---------------------------------------------------------------------#

class multiLevelPercolation:
	
	def __init__(self, _threshold, data, xlen, ylen, zlen, _zFastest, \
	_verbose, _marchingCubesExt, _dataType):
		
		self._threshold = _threshold
		self.data = data
		self.xlen = xlen
		self.ylen = ylen
		self.zlen = zlen
		self._zFastest = _zFastest
		self._verbose = _verbose
		self._marchingCubesExt = _marchingCubesExt
		self._dataType = _dataType
	
	def getThresholdRange(self, _previousThreshold, _maxVal):
		
		# Conduct an order of magnitude analysis
		# This is necessary to ensure that the percolation transition is
		# seen in as few thresholds as possible
		
		# First, determine the order of magnitude of the previous threshold
		# and the maximum value in the threshold range
		_orderOfMagPrev = abs(math.floor(math.log(_previousThreshold, 10)))
		_orderOfMagMax = abs(math.floor(math.log(_maxVal, 10)))
		
		# Calculate the required order of magnitude for the threshold range
		# For instance, if the difference is greater than 1 order of magnitude,
		# required is one greater than the previous threshold
		# This ensures a smooth plot
		# Other cases encountered have been shown below
		# NOTE: All of these were done through trial and error over thousands
		# of structures with different flow cases (stratified ABL, von Karman flow etc). 
		if _orderOfMagMax - _orderOfMagPrev > 1:
			_orderOfMagRequired = _orderOfMagPrev + 1
		elif _orderOfMagMax - _orderOfMagPrev >= 0 and _orderOfMagMax - _orderOfMagPrev <=1:
			_orderOfMagRequired = _orderOfMagPrev + 1
		elif _orderOfMagMax - _orderOfMagPrev < 0:
			_orderOfMagRequired = _orderOfMagMax + 1
		else:
			_orderOfMagRequired = _orderOfMagMax
			
		_tmpList = []
		_tmpList.append(_previousThreshold)

		i = 0
		once = False
		
		# The required order of magnitude dictates the spacing between the thresholds
		# in the list to be tested for percolation analysis
		while True:
			_computedVal = (_maxVal/(10**_orderOfMagRequired))*i
			if _computedVal > _previousThreshold and _computedVal < _maxVal:
				_tmpList.append(_computedVal)
			else:
				if len(_tmpList) > 2:
					break
			i += 1
			if i > 5000: # 5000 is an arbitrarily large value
				# Try again by changing the order of magnitude
				# First increase it
				if _orderOfMagRequired < 10 and not once:
					_orderOfMagRequired = _orderOfMagRequired + 1
				else:
					# Order of magnitude has exceeded 10
					# Try again by decreasing
					_orderOfMagRequired = _orderOfMagRequired - 1
					once = True
				if _orderOfMagRequired < -10:
					print('"\a') # Alert
					print('\n\n\n\n\n ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR \n\n\n\n\n')
					break
					raise SystemError
				i = 0
		return _tmpList[:-1]
	
	def clip_grid(self, n, Q, _structValuedGrid, _lastVal, verbose):
		
		# If the structure is last [0] indexing is not necessary when reading the file
		if _lastVal:
		
			_structureExtent = np.loadtxt('NeighborInformation.txt', skiprows = n-1, dtype = int)

		else:
			
			_structureExtent = np.loadtxt('NeighborInformation.txt', skiprows = n-1, dtype = int)[0]
		
		if verbose:
			print('Original Extent:',_structureExtent)
		
		# Expanded grid is necessary to read and write files properly
		_expandedGrid = 1
		
		_structureExtent[1] += -_expandedGrid
		_structureExtent[2] += _expandedGrid
		_structureExtent[3] += -_expandedGrid
		_structureExtent[4] += _expandedGrid
		_structureExtent[5] += -_expandedGrid
		_structureExtent[6] += _expandedGrid
		
		if _expandedGrid >= 1:
			
			if _structureExtent[1] < 0:
				_structureExtent[1] = 0
			
			if _structureExtent[2] > self.xlen:
				_structureExtent[2] = self.xlen
			
			if _structureExtent[3] < 0:
				_structureExtent[3] = 0
			
			if _structureExtent[4] > self.ylen:
				_structureExtent[4] = self.ylen
			
			if _structureExtent[5] < 0:
				_structureExtent[5] = 0
			
			if _structureExtent[6] > self.zlen:
				_structureExtent[6] = self.zlen
		
		if verbose:
			print('Modified Extent:',_structureExtent)
		
		xlen_structure = _structureExtent[2] - _structureExtent[1]
		ylen_structure = _structureExtent[4] - _structureExtent[3]
		zlen_structure = _structureExtent[6] - _structureExtent[5]
		
		_newGrid = np.zeros((xlen_structure, ylen_structure, zlen_structure), dtype = self._dataType)
		_newGrid = _newGrid.ravel()
		
		# Keep order while reshaping
		if self._zFastest:
			Q = np.reshape(Q, [self.xlen, self.ylen, self.zlen])
		
		else:
			Q = np.reshape(Q, [self.xlen, self.ylen, self.zlen], order = 'F')
			
		Q = Q[_structureExtent[1]:_structureExtent[2], _structureExtent[3]:_structureExtent[4], _structureExtent[5]:_structureExtent[6]]
		Q = Q.ravel()
		
		_structValuedGrid = np.reshape(_structValuedGrid, [self.xlen, self.ylen, self.zlen])
		_structValuedGrid = _structValuedGrid[_structureExtent[1]:_structureExtent[2], _structureExtent[3]:_structureExtent[4], _structureExtent[5]:_structureExtent[6]]
		_structValuedGrid = _structValuedGrid.ravel()
		
		# Reconstruct grid with original values
		for i, val in enumerate(_structValuedGrid):
			
			if val == n:
				
				_newGrid[i] = Q[i]
			
			else:
				
				_newGrid[i] = 0
				
		_newGrid = np.reshape(_newGrid, [xlen_structure, ylen_structure, zlen_structure])
		
		return _newGrid, _structureExtent
	
	def dfStruct(self, n, Q, _structValuedGrid, _lastVal, verbose):
		
		# Clip the grid according to structure dimensions
		_newGrid, _ = self.clip_grid(n, Q, _structValuedGrid, _lastVal, verbose)
		_newGrid = (_newGrid > self._threshold)
		
		# For FD computation, grid dimensions have to be equal
		# Put the _newGrid on to a grid composed of its largest dimension 
		# in every direction
		width = max(np.shape(_newGrid))
		p = np.log(width)/np.log(2)
		p = np.ceil(p)
		width = 2**p			
		
		mz = np.zeros((int(width), int(width), int(width)), dtype = bool)
		mz[:np.shape(_newGrid)[0], :np.shape(_newGrid)[1], :np.shape(_newGrid)[2]] = _newGrid
		_newGrid = mz
		
		boxCountObj = boxCount(_newGrid)
		_n, _r, _df = boxCountObj.calculateBoxCount()		
		
		return _n, _r, _df
		
	def getQualifiedStructures(self, val, Q, _structValuedGrid, lessFD, lessFDval, minVal, verbose):
		
		# Reset existing file	
		boxCountFile = open('box_data.txt','w+')
		boxCountFile.close()
		
		# Get all qualified structures
		_qualifiedStructures = []
		
		for i in range(minVal, len(val)):
			
			boxCountFile = open('box_data.txt','a')
			
			print('Processing: ', i)

			if i == len(val) - 1:

				_lastVal = True

			else:

				_lastVal = False
			
			n, r, df = self.dfStruct(i, Q, _structValuedGrid, _lastVal, verbose)
			
			# Calculate mean and standard deviation for the smallest box sizes
			dfmean = np.mean(df[:2])
			dfstd = np.std(df[:2])
			
			boxCountFile.write(str(i) + ' ' + str(val[i]) + ' ' + str(dfmean) + ' ' + str(dfstd) + '\n')
			boxCountFile.close()
			
			# Filter structures having FD less than a specific value
			if lessFD:
				if dfmean > lessFDval:
					_qualifiedStructures.append(i)

		return _qualifiedStructures
	
	def extract_structure_information(self, _threshVal, data, \
	xlen, ylen, zlen, _zFastest, _verbose, _writeNeighborInformation, \
	_writePercolationData, _marchingCubesExt):
		
		if _writeNeighborInformation:
			
			fw = open('NeighborInformation.txt', 'w+')
			fw.close()
		
		extractStructuresObj = extractStructuresMC(_threshVal, data, \
	xlen, ylen, zlen, _zFastest, _verbose, _writeNeighborInformation, \
	_writePercolationData, _marchingCubesExt)
		structureGrid = extractStructuresObj.extract()
		
		# Return the structValuedGrid and structure counts (volume) information
		u, counts = np.unique(structureGrid, return_counts = True)
		
		return structureGrid, counts
	
	def fullGrid(self, n, Q, _structValuedGrid):
		
		# Place the given structure within the full grid of the domain

		_newGrid = np.zeros((self.xlen, self.ylen, self.zlen), dtype = self._dataType)
		_newGrid = _newGrid.ravel()

		for i, val in enumerate(_structValuedGrid):
			
			if val == n:
				_newGrid[i] = Q[i]
			else:
				_newGrid[i] = 0

		return _newGrid
		
	def addSimpleStructure(self, n, Q, _structValuedGrid):
		
		# Read the simple structures file and add the structure
		_tmpArray = array.array('f')
		_tmpArray.fromfile(open('SimpleStructures.bin', 'rb'), (self.xlen*self.ylen*self.zlen))
		_tmpArray = np.array(_tmpArray)

		_newGrid = self.fullGrid(n, Q, _structValuedGrid)

		# Modify tmpArray with information from newGrid

		for i in range(len(_newGrid)):
			if _newGrid[i]:
				_tmpArray[i] = _newGrid[i]

		fw = open('SimpleStructures.bin', 'wb')
		_tmpArray.tofile(fw)
		fw.close()
	
	def writeComplexStructure(self, n, Q, _structValuedGrid, _percThresh, _lastVal):
		
		# Writes complex structures to file
		# Clip grid ensures file sizes will be small
		_newGrid, _structureExtent = self.clip_grid(n, Q, _structValuedGrid, _lastVal, self._verbose)
		
		_, xmin, xmax, ymin, ymax, zmin, zmax = _structureExtent

		fw = open('IndStructure_' + str(n) + '_' + str(xmin) + '_' + str(xmax) + '_' + str(ymin) + '_' + str(ymax) + '_' + str(zmin) + '_' + str(zmax) + '_' + str(_percThresh) + '.bin', 'wb')
		_newGrid.tofile(fw)
		fw.close()
	
	def processQualifiedStructures(self, _qualifiedStructures, _pthreshold, Q, _structValuedGrid, counts,\
	minVmVval, verbose):
		
		# Create temporary arrays
		_complexStructureIndices = []
		_getPercolationValues = []
		
		# Process all qualified structures
		for i in range(len(_qualifiedStructures)):
			
			# Check for last structure
			if _qualifiedStructures[i] == len(counts) - 1:
				_tmpGrid, _ = self.clip_grid(_qualifiedStructures[i], Q, _structValuedGrid, True, verbose)
			else:
				_tmpGrid, _ = self.clip_grid(_qualifiedStructures[i], Q, _structValuedGrid, False, verbose)

			_xlen, _ylen, _zlen = np.shape(_tmpGrid)
			_tmpGrid = _tmpGrid.ravel()

			_max = np.max(_tmpGrid)
			_threshValList = self.getThresholdRange(_pthreshold, _max)
			
			# Run percolation analysis with the obtained threshold range
			
			percolationObj = percolationAnalysis(_threshValList, _tmpGrid, _xlen, _ylen, _zlen, \
			self._zFastest, self._verbose, self._marchingCubesExt)
			percolationObj.processThresholds()

			# Read Percolation threshold file and get min(VmV)
			data = np.loadtxt('Percolation_threshold.txt')
			alpha = data[:, 0]
			Vmax = data[:, 1]
			V = data[:, 2]

			VmV = Vmax / V
			
			# Identify the fist minimum
			minVal = 0
			once = False
			for ip in range(len(VmV)):
				if ip == 0:
					minVal = VmV[ip]
				else:
					if VmV[ip] < minVal and not once:
						minVal = VmV[ip]
					elif VmV[ip] > 0.9:
						once = True

			if minVal > minVmVval:
				
				if self._verbose:
					print('Simple Structure with Vmax/V:' + str(minVal))
				self.addSimpleStructure(_qualifiedStructures[i], Q, _structValuedGrid)
				fw = open('log.txt', 'a')
				fw.write(str(_qualifiedStructures[i]) + ': Simple' + '\n')
				fw.close()

			else:

				# Limit range with minimum value of VmV
				# It considers the first minimum
				_minWhere = np.where(np.in1d(VmV, minVal))[0][0]
				VmV = VmV[:_minWhere + 1]
				alpha = alpha[:_minWhere + 1]

				slope = abs(np.diff(VmV) / np.diff(alpha))
				maxslope = max(slope)
				slopeIndex = np.where(np.in1d(slope, maxslope))[0]

				_perc = np.mean([alpha[slopeIndex[0]], alpha[slopeIndex[0]+1]])

				_getPercolationValues.append(_perc)

				_complexStructureIndices.append(_qualifiedStructures[i])
				if _qualifiedStructures[i] == len(counts) - 1:
					self.writeComplexStructure(_qualifiedStructures[i], Q, _structValuedGrid, _perc, True)
				else:
					self.writeComplexStructure(_qualifiedStructures[i], Q, _structValuedGrid, _perc, False)
				fw = open('log.txt', 'a')
				fw.write(str(_qualifiedStructures[i]) + '_' +  str(_perc) +  ': Complex' + '\n')
				fw.close()
				
			# Rename percolation threshold files for later inspection
			os.system('mv Percolation_threshold.txt Percolation_threshold'+str(i)+'.txt')
			os.system('rm -rf Percolation_threshold.txt')
		
	def getSimpleStructures(self, lessFD, lessFDval, minVmVval, _cleanup):
		
		# Extract structures first with neighbor information and without
		# percolation data
		
		_writeNeighborInformation = True
		_writePercolationData = False
		
		_structValuedGrid, counts = self.extract_structure_information(self._threshold, self.data, \
	self.xlen, self.ylen, self.zlen, self._zFastest, self._verbose, \
	_writeNeighborInformation, _writePercolationData, self._marchingCubesExt)
		
		# Filter all structures having a fractal dimension less than a specific value
		# This gives a list of the qualified structures for further analysis
		
		# Set minVal to 1. 0 is empty space. 
		minVal = 1
		
		_qualifiedStructures = self.getQualifiedStructures(counts, self.data, _structValuedGrid, lessFD, \
		lessFDval, minVal, self._verbose)
		
		# For first run, create simple structures grid with zeros
		fw = open('SimpleStructures.bin', 'wb')
		_tmpGrid = np.zeros((self.xlen, self.ylen, self.zlen), dtype = self._dataType)
		_tmpGrid = _tmpGrid.ravel()
		_tmpGrid.tofile(fw)
		fw.close()
		
		self.processQualifiedStructures(_qualifiedStructures, self._threshold, self.data, _structValuedGrid, counts, minVmVval,\
		self._verbose)
		
		# Run while loop on all remaining structures
		while True:
			
			# Get all IndStructure files
			_files = os.listdir('.')
			_files = [i for i in _files if 'IndStructure' in i]

			# Sort files in order of the highest threshold
			_files.sort(key = lambda f:np.float32(f.split('_')[-1].split('.bin')[0]))
			_files = _files[::-1]
			
			if not _files:
				break # When no IndStructure files are present, the while loop is broken
			else:
				_filenameRead = _files[0]
			
			# Write running file to log
			fw = open('log.txt', 'a')
			fw.write('Running: ' + _filenameRead + '\n')
			fw.close()
			
			# Get structure extents
			xmin = int(_filenameRead.split('_')[2])
			xmax = int(_filenameRead.split('_')[3])
			ymin = int(_filenameRead.split('_')[4])
			ymax = int(_filenameRead.split('_')[5])
			zmin = int(_filenameRead.split('_')[6])
			zmax = int(_filenameRead.split('_')[7])
			
			xlen = xmax - xmin
			ylen = ymax - ymin
			zlen = zmax - zmin
			
			if self._verbose:
				print('Processing file: ' + _filenameRead)
			
			# Read data from file
			Q = array.array('f')
			Q.fromfile(open(_filenameRead, 'rb'), (xlen*ylen*zlen*4) // 4)

			Q = np.array(Q, dtype = self._dataType)

			_min = np.min(Q)
			_max = np.max(Q)
			
			Q = np.reshape(Q, [xlen, ylen, zlen])
			
			# Put the structure in the original grid
			_tmpGrid = np.zeros((self.xlen, self.ylen, self.zlen), dtype = self._dataType)
			
			_tmpGrid[xmin:xmax, ymin:ymax, zmin:zmax] = Q
			Q = _tmpGrid.ravel()
			
			# Get threshold from filename
			_gthreshValList = [np.float32(_filenameRead.split('_')[-1].split('.bin')[0])]
			
			# Extract structures first with neighbor information and without
			# percolation data
			_writeNeighborInformation = True
			_writePercolationData = False
			
			_structValuedGrid, counts = self.extract_structure_information(_gthreshValList[0], Q, \
		self.xlen, self.ylen, self.zlen, self._zFastest, self._verbose, \
		_writeNeighborInformation, _writePercolationData, self._marchingCubesExt)
			
			# Repeat same steps as before
			_qualifiedStructures = self.getQualifiedStructures(counts, Q, _structValuedGrid, lessFD, \
			lessFDval, minVal, self._verbose)
			
			self.processQualifiedStructures(_qualifiedStructures, _gthreshValList[0], Q, _structValuedGrid, counts, minVmVval,\
			self._verbose)
			
			os.system('rm -rf '+_filenameRead)
		
		# Clean up
		os.system('rm -rf box_data.txt Neighbor*.txt')
		if _cleanup:
			os.system('rm -rf Percolation*.txt')
		
		print('Done..')
	
	@staticmethod
	@jit(nopython=True)	
	def getIndividualThresholds(data, _structValuedGrid):
		
		maxVal = _structValuedGrid.max()
		
		data = data.ravel()
		_structValuedGrid = _structValuedGrid.ravel()
		
		minThreshVals = np.zeros(maxVal, dtype = np.float64)
		
		for i in range(1, maxVal+1):
			minThreshVal = 0
			
			for j in range(len(_structValuedGrid)):
				if _structValuedGrid[j] == i:
					if minThreshVal == 0:
						minThreshVal += data[j]
					else:
						if data[j] < minThreshVal:
							minThreshVal = data[j]
			
			minThreshVals[i-1] = minThreshVal
		
		return minThreshVals
