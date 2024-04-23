from extractStructuresWithMC import extractStructuresMC
import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------------------#

# ---------Analysis of Multiscale Data from the Geosciences---------- #

# Author: Abhishek Harikrishnan
# Email: abhishek.harikrishnan@fu-berlin.de
# Last updated: 22-04-2024

#---------------------------------------------------------------------#

class percolationAnalysis:
	
	def __init__(self, _threshVals, c, xlen, ylen, zlen, _zFastest, \
	verbose, _marchingCubesExt):
		
		# By default set _writePercolationData = True and 
		# _writeNeighborInformation = False. Neighbor information is
		# not necessary as it will be overwritten anyway.
		
		self._writePercolationData = True
		self._writeNeighborInformation = False
		
		self._threshVals = _threshVals
		self.c = c
		self.xlen = xlen
		self.ylen = ylen
		self.zlen = zlen
		self._zFastest = _zFastest
		self.verbose = verbose
		self._marchingCubesExt = _marchingCubesExt
		
	def processThresholds(self):
		
		# Reset the file
		fw = open('Percolation_threshold.txt', 'w+')
		fw.close()
		
		for i, _threshVal in enumerate(self._threshVals):
			
			if self.verbose:
				print('Processing threshold:', _threshVal)		
		
			# Initialize extraction script
			extractStructuresObj = extractStructuresMC(_threshVal, self.c, \
self.xlen, self.ylen, self.zlen, self._zFastest, self.verbose, \
self._writeNeighborInformation, self._writePercolationData, self._marchingCubesExt)

			# Compute V_max and V
			extractStructuresObj.extract()
			
	def plotPercolation(self, _filename):
		
		data = np.loadtxt(_filename)
		
		# Get the thresholds, Vmax and V
		alpha = data[:, 0]
		Vmax = data[:, 1]
		V = data[:, 2]

		# Sort the data based on thresholds in alpha
		# Useful if multiprocessing is used for different thresholds and
		# the data is not written in the correct order
		_indices = sorted(range(len(alpha)), key=lambda k: alpha[k])
		alpha = alpha[_indices]
		Vmax = Vmax[_indices]
		V = V[_indices]
		
		# Set plot parameters
		plt.rc('text', usetex=True)
		plt.rc('font', family='serif')
		ax = plt.figure().gca()
		
		# Calculate ratio Vmax/V
		VmV = Vmax / V
		
		# Calculate slope and get max slope index
		slope = abs(np.diff(Vmax/V) / np.diff(alpha))
		maxslope = max(slope)
		slopeIndex = np.where(np.in1d(slope, maxslope))[0]
		
		if self.verbose:
			print('Min, Max:', alpha[slopeIndex[0]], alpha[slopeIndex[0]+1])
			print('Mean:', np.mean([alpha[slopeIndex[0]], alpha[slopeIndex[0]+1]]))

		ax.loglog(alpha, VmV, '-.b', linewidth = 0.5)
		ax.axvspan(alpha[slopeIndex[0]], alpha[slopeIndex[0]+1], alpha=0.5, color='blue')
		ax.set_ylim([min(VmV), 1])
		ax.set_xlabel(r'$\tau$')
		ax.set_ylabel(r'$V_{max}/V$')
		plt.show()
		
		# Return min, max and mean data
		return alpha[slopeIndex[0]], alpha[slopeIndex[0]+1], np.mean([alpha[slopeIndex[0]], alpha[slopeIndex[0]+1]])
