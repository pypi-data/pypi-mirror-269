import numpy as np
import time
import array
import copy
import time	
# from MCOutliers import outliers

#---------------------------------------------------------------------#

# ---------Analysis of Multiscale Data from the Geosciences---------- #

# Author: Abhishek Harikrishnan
# Email: abhishek.harikrishnan@fu-berlin.de
# Last updated: 06-12-2023

#---------------------------------------------------------------------#

class extractStructuresMC:
	
	def __init__(self, _threshVal, c, xlen, ylen, zlen, _zFastest, \
	verbose, _writeNeighborInformation,	_writePercolationData, \
	_marchingCubesExt):
		
		self.verbose = verbose
		self._marchingCubesExt = _marchingCubesExt
		self._writeNeighborInformation = _writeNeighborInformation
		self._writePercolationData = _writePercolationData
		if self._marchingCubesExt:
			print('Marching cubes correction enabled..')
		else:
			print('Marching cubes correction NOT enabled..')
		self._threshVal = _threshVal
		if self.verbose:
			print('Chosen threshold:', _threshVal)
		
		self.xlen = xlen
		self.ylen = ylen
		self.zlen = zlen
		if self.verbose:
			print('Data is of shape: ' + str(xlen) + ', ' + str(ylen) + ', '\
		 + str(zlen))
		
		# Reshape data
		if _zFastest:
			self.c = np.reshape(c, [self.xlen, self.ylen, self.zlen])
		else:
			self.c = np.reshape(c, [self.xlen, self.ylen, self.zlen], order = 'F')
			
		# Threshold the scalar field based on the sign of the value
		if _threshVal > 0:
			self.c = (self.c > self._threshVal)
		else:
			self.c = (self.c < self._threshVal)
		
		# Pad array with zeros in all dimensions
		mz = np.zeros((xlen + 1, ylen + 1, zlen + 1), dtype = bool)
		mz[:np.shape(self.c)[0], :np.shape(self.c)[1], :np.shape(self.c)[2]] = self.c
		self.c = mz
		
	def outliers(self, _whichOne):

		outliers = [[], # 0
		[], # 1
		[], # 2
		[], # 3
		[], # 4
		[[0], [2]], # 5
		[], # 6
		[], # 7
		[], # 8
		[], # 9
		[[1], [3]], # 10
		[], # 11
		[], # 12
		[], # 13
		[], # 14
		[], # 15
		[], # 16
		[], # 17
		[[1], [4]], # 18
		[], # 19
		[[2], [4]], # 20
		[[0, 4], [2]], # 21
		[[1, 2], [4]], # 22
		[], # 23
		[[3], [4]], # 24
		[], # 25
		[[1], [3], [4]], # 26
		[], # 27
		[[2, 3], [4]], # 28
		[], # 29
		[[1, 2, 3], [4]], # 30
		[], # 31
		[], # 32
		[[0], [5]], # 33
		[], # 34
		[], # 35
		[[2], [5]], # 36
		[[0], [2], [5]], # 37
		[], # 38
		[], # 39
		[[3], [5]], # 40
		[[0, 3], [5]], # 41
		[[1, 5], [3]], # 42
		[], # 43
		[[2, 3], [5]], # 44
		[[0, 2, 3], [5]], # 45
		[], # 46
		[], # 47
		[], # 48
		[], # 49
		[], # 50
		[], # 51
		[[2], [4, 5]], # 52
		[[2], [0, 4, 5]], # 53
		[], # 54
		[], # 55
		[[3], [4, 5]], # 56
		[], # 57
		[[3], [1, 4, 5]], # 58
		[], # 59
		[[2, 3], [4, 5]], # 60
		[], # 61
		[], # 62
		[], # 63
		[], # 64
		[[0], [6]], # 65
		[[1], [6]], # 66
		[[0, 1], [6]], # 67
		[], # 68
		[[0], [2, 6]], # 69
		[], # 70
		[], # 71
		[[3], [6]], # 72
		[[0, 3], [6]], # 73
		[[1], [3], [6]], # 74
		[[0, 1, 3], [6]], # 75
		[], # 76
		[], # 77
		[], # 78
		[], # 79
		[[4], [6]], # 80
		[[0, 4], [6]], # 81
		[[1], [4], [6]], # 82
		[[0, 1, 4], [6]], # 83
		[[4], [2, 6]], # 84
		[[0, 4], [2, 6]], # 85
		[[1, 2, 6], [4]], # 86
		[], # 87
		[[3], [4], [6]], # 88
		[[0, 3, 4], [6]], # 89
		[[1], [3], [4], [6]], # 90
		[[0, 1, 3, 4], [6]], # 91 
		[[2, 3, 6], [4]], # 92
		[], # 93
		[[1, 2, 3, 6], [4]], # 94
		[], # 95
		[], # 96
		[[0], [5, 6]], # 97
		[], # 98
		[], # 99
		[], # 100
		[[0], [2, 5, 6]], # 101
		[], # 102
		[], # 103
		[[3], [5, 6]], # 104
		[[0, 3], [5, 6]], # 105
		[[3], [1, 5, 6]], # 106
		[], # 107
		[], # 108
		[], # 109
		[], # 110
		[], # 111
		[], # 112
		[], # 113
		[], # 114
		[], # 115
		[], # 116
		[], # 117
		[], # 118
		[], # 119
		[[3], [4, 5, 6]], # 120
		[], # 121
		[[3], [1, 4, 5, 6]], # 122
		[], # 123
		[], # 124
		[[1], [7]], # 125
		[], # 126
		[], # 127
		[], # 128
		[[0], [7]], # 129
		[[1], [7]], # 130
		[[0, 1], [7]], # 131
		[[2], [7]], # 132
		[[0], [2], [7]], # 133
		[[1, 2], [7]], # 134
		[[0, 1, 2], [7]], # 135
		[], # 136
		[], # 137
		[[1], [3, 7]], # 138
		[], # 139
		[], # 140
		[], # 141
		[], # 142
		[], # 143
		[], # 144
		[], # 145
		[[1], [4, 7]], # 146
		[], # 147
		[[2], [4, 7]], # 148
		[[2], [0, 4, 7]], # 149
		[[1, 2], [4, 7]], # 150
		[], # 151
		[], # 152
		[], # 153
		[[1], [3, 4, 7]], # 154
		[], # 155
		[], # 156
		[], # 157
		[], # 158
		[], # 159
		[[5], [7]], # 160
		[[0], [5], [7]], # 161
		[[1, 5], [7]], # 162
		[[0, 1, 5], [7]], # 163
		[[2], [5], [7]], # 164
		[[0], [2], [5], [7]], # 165
		[[1, 2, 5], [7]], # 166
		[[0, 1, 2, 5], [7]], # 167
		[[3, 7], [5]], # 168
		[[0, 3, 7], [5]], # 169
		[[1, 5], [3, 7]], # 170
		[], # 171
		[[2, 3, 7], [5]], # 172
		[[0, 2, 3, 7], [5]], # 173
		[], # 174
		[], # 175
		[], # 176
		[], # 177
		[], # 178
		[], # 179
		[[2], [4, 5, 7]], # 180
		[[2], [0, 4, 5, 7]], # 181
		[], # 182
		[], # 183
		[], # 184
		[], # 185
		[], # 186
		[], # 187
		[], # 188
		[], # 189
		[[0], [6]], # 190
		[], # 191
		[], # 192
		[[0], [6, 7]], # 193
		[[1], [6, 7]], # 194
		[[0, 1], [6, 7]], # 195
		[], # 196
		[[0], [2, 6, 7]], # 197
		[], # 198
		[], # 199
		[], # 200
		[], # 201
		[[1], [3, 6, 7]], # 202
		[], # 203
		[], # 204
		[], # 205
		[], # 206
		[], # 207
		[], # 208
		[], # 209
		[[1], [4, 6, 7]], # 210
		[], # 211
		[], # 212
		[], # 213
		[], # 214
		[[3], [5]], # 215
		[], # 216
		[], # 217
		[[1], [3, 4, 6, 7]], # 218
		[], # 219
		[], # 220
		[], # 221
		[], # 222
		[], # 223
		[], # 224
		[[0], [5, 6, 7]], # 225
		[], # 226
		[], # 227
		[], # 228
		[[0], [2, 5, 6, 7]], # 229
		[], # 230
		[], # 231
		[], # 232
		[], # 233
		[], # 234
		[[2], [4]], # 235
		[], # 236
		[], # 237
		[], # 238
		[], # 239
		[], # 240
		[], # 241
		[], # 242
		[], # 243
		[], # 244
		[], # 245
		[], # 246
		[], # 247
		[], # 248
		[], # 249
		[], # 250
		[], # 251
		[], # 252
		[], # 253
		[], # 254
		[], # 255
		]
		
		return outliers[_whichOne]
	
	def find_case_number(self, _cube):
											
		return sum(2**v for v in range(8) if _cube[v] == True)
	
	def extract(self):

		# Start timer

		start_time = time.time()

		# All boxes satisfying the thresholding criterion are checked
		# for their neighboring cells (26 - 6 faces, 12 edges, 8 corners). 

		_structVal = 0
		_structValuedGrid = np.zeros((self.xlen + 1, self.ylen + 1, \
		self.zlen + 1), dtype = np.uint32)	# uint32 has values from 0 upto 4294967295
		_outlierCaseCount = 0

		for i in range(self.xlen + 1):
			for j in range(self.ylen + 1):
				for k in range(self.zlen + 1):
					
					if self.c[i,j,k]:
						
						if not _structValuedGrid[i,j,k] > 0:
							
								_structVal += 1
								
								if self.verbose:
									print(_structVal)
								
								_neighborVal = []
								_structValuedGrid[i,j,k] = _structVal
								
								_loopCounter = 0
								_neighborCounter = 0
								
								_origiVal = i
								_origjVal = j
								_origkVal = k
								
								while True:
									
									# Reset all corner flags
								
									_c1 = False
									_c2 = False
									_c3 = False
									_c4 = False
									_c5 = False
									_c6 = False
									_c7 = False
									_c8 = False
								
									# Reset all face flags
								
									_f1 = False
									_f2 = False
									_f3 = False
									_f4 = False
									_f5 = False
									_f6 = False
									
									# Reset all edge flags
									
									_e1 = False
									_e2 = False
									_e3 = False
									_e4 = False
									_e5 = False
									_e6 = False
									_e7 = False
									_e8 = False
									_e9 = False
									_e10 = False
									_e11 = False
									_e12 = False
									
									_numberOfNeighbors = 0
									
									# Create aux cube [3, 3, 3]
								
									_i = 0
									_j = 0
									_k = 0
									_auxCube = np.zeros((3, 3, 3))
									
									if _loopCounter > 0:
										
										try:
										
											i = _neighborVal[_neighborCounter][0]
											j = _neighborVal[_neighborCounter][1]
											k = _neighborVal[_neighborCounter][2]
											
											_neighborCounter += 1
										
										except IndexError:
											
											break
									
									# Faces
									
									try:
										
										if self.c[i+1,j,k]:
											
											if not _structValuedGrid[i+1, j, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j,k] = _structVal
												_auxCube[_i+1,_j,_k] = 1
												_f1 = True
									
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j,k]:
											
											if not _structValuedGrid[i-1, j, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j,k] = _structVal
												_auxCube[_i-1,_j,_k] = 1
												_f2 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i,j+1,k]:
											
											if not _structValuedGrid[i, j+1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j+1,k] = _structVal
												_auxCube[_i,_j+1,_k] = 1
												_f3 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i,j-1,k]:
											
											if not _structValuedGrid[i, j-1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j-1,k] = _structVal
												_auxCube[_i,_j-1,_k] = 1
												_f4 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i,j,k+1]:
											
											if not _structValuedGrid[i, j, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j,k+1] = _structVal
												_auxCube[_i,_j,_k+1] = 1
												_f5 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i,j,k-1]:
											
											if not _structValuedGrid[i, j, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j,k-1] = _structVal
												_auxCube[_i,_j,_k-1] = 1
												_f6 = True
									
									except IndexError:
										
										pass
										
									# Edges
									
									try:
										
										if self.c[i+1,j+1,k]:
											
											if not _structValuedGrid[i+1, j+1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j+1,k] = _structVal
												_auxCube[_i+1,_j+1,_k] = 1
												_e1 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i+1,j-1,k]:
											
											if not _structValuedGrid[i+1, j-1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j-1,k] = _structVal
												_auxCube[_i+1,_j-1,_k] = 1
												_e2 = True
									
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i-1,j+1,k]:
											
											if not _structValuedGrid[i-1, j+1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j+1,k] = _structVal
												_auxCube[_i-1,_j+1,_k] = 1
												_e3 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i-1,j-1,k]:
											
											if not _structValuedGrid[i-1, j-1, k] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j-1,k] = _structVal
												_auxCube[_i-1,_j-1,_k] = 1
												_e4 = True
									
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i+1,j,k+1]:
											
											if not _structValuedGrid[i+1, j, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j,k+1] = _structVal
												_auxCube[_i+1,_j,_k+1] = _structVal
												_e5 = True
									
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j,k+1]:
											
											if not _structValuedGrid[i-1, j, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j,k+1] = _structVal
												_auxCube[_i-1,_j,_k+1] = 1
												_e6 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i,j+1,k+1]:
											
											if not _structValuedGrid[i, j+1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j+1,k+1] = _structVal
												_auxCube[_i,_j+1,_k+1] = 1
												_e7 = True
									
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i,j-1,k+1]:
											
											if not _structValuedGrid[i, j-1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j-1,k+1] = _structVal
												_auxCube[_i,_j-1,_k+1] = 1
												_e8 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i+1,j,k-1]:
											
											if not _structValuedGrid[i+1, j, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j,k-1] = _structVal
												_auxCube[_i+1,_j,_k-1] = 1
												_e9 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i-1,j,k-1]:
											
											if not _structValuedGrid[i-1, j, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j,k-1] = _structVal
												_auxCube[_i-1,_j,_k-1] = 1
												_e10 = True
												
									except IndexError:
										
										pass
									
									try:
										
										if self.c[i,j+1,k-1]:
											
											if not _structValuedGrid[i, j+1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j+1,k-1] = _structVal
												_auxCube[_i,_j+1,_k-1] = 1
												_e11 = True
									
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i,j-1,k-1]:
											
											if not _structValuedGrid[i, j-1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i,j-1,k-1] = _structVal
												_auxCube[_i,_j-1,_k-1] = 1
												_e12 = True
												
									except IndexError:
										
										pass
										
									# Corners
									
									try:
										
										if self.c[i+1,j+1,k+1]:
											
											if not _structValuedGrid[i+1, j+1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j+1,k+1] = _structVal
												_auxCube[_i+1,_j+1,_k+1] = 1
												_c1 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i+1,j-1,k+1]:
											
											if not _structValuedGrid[i+1, j-1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j-1,k+1] = _structVal
												_auxCube[_i+1,_j-1,_k+1] = 1
												_c2 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j+1,k+1]:
											
											if not _structValuedGrid[i-1, j+1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j+1,k+1] = _structVal
												_auxCube[_i-1,_j+1,_k+1] = 1
												_c3 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j-1,k+1]:
											
											if not _structValuedGrid[i-1, j-1, k+1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j-1,k+1] = _structVal
												_auxCube[_i-1,_j-1,_k+1] = 1
												_c4 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i+1,j+1,k-1]:
											
											if not _structValuedGrid[i+1, j+1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j+1,k-1] = _structVal
												_auxCube[_i+1,_j+1,_k-1] = 1
												_c5 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i+1,j-1,k-1]:
											
											if not _structValuedGrid[i+1, j-1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i+1,j-1,k-1] = _structVal
												_auxCube[_i+1,_j-1,_k-1] = 1
												_c6 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j+1,k-1]:
											
											if not _structValuedGrid[i-1, j+1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j+1,k-1] = _structVal
												_auxCube[_i-1,_j+1,_k-1] = 1
												_c7 = True
												
									except IndexError:
										
										pass
										
									try:
										
										if self.c[i-1,j-1,k-1]:
											
											if not _structValuedGrid[i-1, j-1, k-1] > 0:
											
												_numberOfNeighbors += 1
												_structValuedGrid[i-1,j-1,k-1] = _structVal
												_auxCube[_i-1,_j-1,_k-1] = 1
												_c8 = True
												
									except IndexError:
										
										pass
									
									if self._marchingCubesExt:
									
										# Marching cubes extension
										# All the points are checked again to see how the surface mesh is constructed
										
										_cornerFlags = [_c1, _c2, _c3, _c4, _c5, _c6, _c7, _c8]
										_faceFlags = [_f1, _f2, _f3, _f4, _f5, _f6]
										_edgeFlags = [_e1, _e2, _e3, _e4, _e5, _e6, _e7, _e8, _e9, _e10, _e11, _e12]
										
										_cube1 = [_f6, _e9, _c6, _e12, True, _f1, _e2, _f4]
										_cube2 = [_e10, _f6, _e12, _c8, _f2, True, _f4, _e4]
										_cube3 = [_c7, _e11, _f6, _e10, _e3, _f3, True, _f2]
										_cube4 = [_e11, _c5, _e9, _f6, _f3, _e1, _f1, True]
										_cube5 = [True, _f1, _e2, _f4, _f5, _e5, _c2, _e8]
										_cube6 = [_f2, True, _f4, _e4, _e6, _f5, _e8, _c4]
										_cube7 = [_e3, _f3, True, _f2, _c3, _e7, _f5, _e6]
										_cube8 = [_f3, _e1, _f1, True, _e7, _c1, _e5, _f5]
										
										# Identify the cases of the cube
										
										_cases = [self.find_case_number(_cube1), self.find_case_number(_cube2), \
										self.find_case_number(_cube3), self.find_case_number(_cube4), \
										self.find_case_number(_cube5), self.find_case_number(_cube6), \
										self.find_case_number(_cube7), self.find_case_number(_cube8)]
										
										sysErrFlag = False
										
										for ii in range(8):
											
											_caseVal = self.outliers(_cases[ii])
											
											if len(_caseVal) > 0:
												
												sysErrFlag = True
												_outlierCaseCount += 1
												
												# Keep the points which contain [i, j, k]. Discard all remaining ones.
												# NOTE: [i, j, k] differs for all cubes.
												
												if ii == 0: # corresponding to cube 1
													for jj in range(len(_caseVal)):
														if 4 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 0:
																	_structValuedGrid[i, j, k-1] = 0
																	_auxCube[_i, _j, _k-1] = 0
																if _removeVal[kk] == 1:
																	_structValuedGrid[i+1, j, k-1] = 0
																	_auxCube[_i+1, _j, _k-1] = 0
																if _removeVal[kk] == 2:
																	_structValuedGrid[i+1, j-1, k-1] = 0
																	_auxCube[_i+1, _j-1, _k-1] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i, j-1, k-1] = 0
																	_auxCube[_i, _j-1, _k-1] = 0
																if _removeVal[kk] == 5:
																	_structValuedGrid[i+1, j, k] = 0
																	_auxCube[_i+1, _j, _k] = 0
																if _removeVal[kk] == 6:
																	_structValuedGrid[i+1, j-1, k] = 0
																	_auxCube[_i+1, _j-1, _k] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i, j-1, k] = 0
																	_auxCube[_i, _j-1, _k] = 0
												
												if ii == 1: # corresponding to cube 2
													for jj in range(len(_caseVal)):
														if 5 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 0:
																	_structValuedGrid[i-1, j, k-1] = 0
																	_auxCube[_i-1, _j, _k-1] = 0
																if _removeVal[kk] == 1:
																	_structValuedGrid[i, j, k-1] = 0
																	_auxCube[_i, _j, _k-1] = 0
																if _removeVal[kk] == 2:
																	_structValuedGrid[i, j-1, k-1] = 0
																	_auxCube[_i, _j-1, _k-1] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i-1, j-1, k-1] = 0
																	_auxCube[_i-1, _j-1, _k-1] = 0
																if _removeVal[kk] == 4:
																	_structValuedGrid[i-1, j, k] = 0
																	_auxCube[_i-1, _j, _k] = 0
																if _removeVal[kk] == 6:
																	_structValuedGrid[i, j-1, k] = 0
																	_auxCube[_i, _j-1, _k] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i-1, j-1, k] = 0
																	_auxCube[_i-1, _j-1, _k] = 0
												
												if ii == 2: # corresponding to cube 3
													for jj in range(len(_caseVal)):
														if 6 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 0:
																	_structValuedGrid[i-1, j+1, k-1] = 0
																	_auxCube[_i-1, _j+1, _k-1] = 0
																if _removeVal[kk] == 1:
																	_structValuedGrid[i, j+1, k-1] = 0
																	_auxCube[_i, _j+1, _k-1] = 0
																if _removeVal[kk] == 2:
																	_structValuedGrid[i, j, k-1] = 0
																	_auxCube[_i, _j, _k-1] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i-1, j, k-1] = 0
																	_auxCube[_i-1, _j, _k-1] = 0
																if _removeVal[kk] == 4:
																	_structValuedGrid[i-1, j+1, k] = 0
																	_auxCube[_i-1, _j+1, _k] = 0
																if _removeVal[kk] == 5:
																	_structValuedGrid[i, j+1, k] = 0
																	_auxCube[_i, _j+1, _k] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i-1, j, k] = 0
																	_auxCube[_i-1, _j, _k] = 0
												
												if ii == 3: # corresponding to cube 4
													for jj in range(len(_caseVal)):
														if 7 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																	if _removeVal[kk] == 0:
																		_structValuedGrid[i, j+1, k-1] = 0
																		_auxCube[_i, _j+1, _k-1] = 0
																	if _removeVal[kk] == 1:
																		_structValuedGrid[i+1, j+1, k-1] = 0
																		_auxCube[_i+1, _j+1, _k-1] = 0
																	if _removeVal[kk] == 2:
																		_structValuedGrid[i+1, j, k-1] = 0
																		_auxCube[_i+1, _j, _k-1] = 0
																	if _removeVal[kk] == 3:
																		_structValuedGrid[i, j, k-1] = 0
																		_auxCube[_i, _j, _k-1] = 0
																	if _removeVal[kk] == 4:
																		_structValuedGrid[i, j+1, k] = 0
																		_auxCube[_i, _j+1, _k] = 0
																	if _removeVal[kk] == 5:
																		_structValuedGrid[i+1, j+1, k] = 0
																		_auxCube[_i+1, _j+1, _k] = 0
																	if _removeVal[kk] == 6:
																		_structValuedGrid[i+1, j, k] = 0
																		_auxCube[_i+1, _j, _k] = 0
												
												if ii == 4: # corresponding to cube 5
													for jj in range(len(_caseVal)):
														if 0 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 1:
																	_structValuedGrid[i+1, j, k] = 0
																	_auxCube[_i+1, _j, _k] = 0
																if _removeVal[kk] == 2:
																	_structValuedGrid[i+1, j-1, k] = 0
																	_auxCube[_i+1, _j-1, _k] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i, j-1, k] = 0
																	_auxCube[_i, _j-1, _k] = 0
																if _removeVal[kk] == 4:
																	_structValuedGrid[i, j, k+1] = 0
																	_auxCube[_i, _j, _k+1] = 0
																if _removeVal[kk] == 5:
																	_structValuedGrid[i+1, j, k+1] = 0
																	_auxCube[_i+1, _j, _k+1] = 0
																if _removeVal[kk] == 6:
																	_structValuedGrid[i+1, j-1, k+1] = 0
																	_auxCube[_i+1, _j-1, _k+1] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i, j-1, k+1] = 0
																	_auxCube[_i, _j-1, _k+1] = 0
												
												if ii == 5: # corresponding to cube 6
													for jj in range(len(_caseVal)):
														if 1 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 0:
																	_structValuedGrid[i-1, j, k] = 0
																	_auxCube[_i-1, _j, _k] = 0
																if _removeVal[kk] == 2:
																	_structValuedGrid[i, j-1, k] = 0
																	_auxCube[_i, _j-1, _k] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i-1, j-1, k] = 0
																	_auxCube[_i-1, _j-1, _k] = 0
																if _removeVal[kk] == 4:
																	_structValuedGrid[i-1, j, k+1] = 0
																	_auxCube[_i-1, _j, _k+1] = 0
																if _removeVal[kk] == 5:
																	_structValuedGrid[i, j, k+1] = 0
																	_auxCube[_i, _j, _k+1] = 0
																if _removeVal[kk] == 6:
																	_structValuedGrid[i, j-1, k+1] = 0
																	_auxCube[_i, _j-1, _k+1] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i-1, j-1, k+1] = 0
																	_auxCube[_i-1, _j-1, _k+1] = 0
												
												if ii == 6: # corresponding to cube 7
													for jj in range(len(_caseVal)):
														if 2 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																if _removeVal[kk] == 0:
																	_structValuedGrid[i-1, j+1, k] = 0
																	_auxCube[_i-1, _j+1, _k] = 0
																if _removeVal[kk] == 1:
																	_structValuedGrid[i, j+1, k] = 0
																	_auxCube[_i, _j+1, _k] = 0
																if _removeVal[kk] == 3:
																	_structValuedGrid[i-1, j, k] = 0
																	_auxCube[_i-1, _j, _k] = 0
																if _removeVal[kk] == 4:
																	_structValuedGrid[i-1, j+1, k+1] = 0
																	_auxCube[_i-1, _j+1, _k+1] = 0
																if _removeVal[kk] == 5:
																	_structValuedGrid[i, j+1, k+1] = 0
																	_auxCube[_i, _j+1, _k+1] = 0
																if _removeVal[kk] == 6:
																	_structValuedGrid[i, j, k+1] = 0
																	_auxCube[_i, _j, _k+1] = 0
																if _removeVal[kk] == 7:
																	_structValuedGrid[i-1, j, k+1] = 0
																	_auxCube[_i-1, _j, _k+1] = 0
												
												if ii == 7: # corresponding to cube 8
													for jj in range(len(_caseVal)):
														if 3 not in _caseVal[jj]:
															_removeVal = _caseVal[jj]
															for kk in range(len(_removeVal)):
																	if _removeVal[kk] == 0:
																		_structValuedGrid[i, j+1, k] = 0
																		_auxCube[_i, _j+1, _k] = 0
																	if _removeVal[kk] == 1:
																		_structValuedGrid[i+1, j+1, k] = 0
																		_auxCube[_i+1, _j+1, _k] = 0
																	if _removeVal[kk] == 2:
																		_structValuedGrid[i+1, j, k] = 0
																		_auxCube[_i+1, _j, _k] = 0
																	if _removeVal[kk] == 4:
																		_structValuedGrid[i, j+1, k+1] = 0
																		_auxCube[_i, _j+1, _k+1] = 0
																	if _removeVal[kk] == 5:
																		_structValuedGrid[i+1, j+1, k+1] = 0
																		_auxCube[_i+1, _j+1, _k+1] = 0
																	if _removeVal[kk] == 6:
																		_structValuedGrid[i+1, j, k+1] = 0
																		_auxCube[_i+1, _j, _k+1] = 0
																	if _removeVal[kk] == 7:
																		_structValuedGrid[i, j, k+1] = 0
																		_auxCube[_i, _j, _k+1] = 0
									
									if _auxCube[_i+1,_j,_k]:
										_neighborVal.append([i+1,j,k])
											
									if _auxCube[_i-1,_j,_k]:
										_neighborVal.append([i-1,j,k])
											
									if _auxCube[_i,_j+1,_k]:
										_neighborVal.append([i,j+1,k])
											
									if _auxCube[_i,_j-1,_k]:
										_neighborVal.append([i,j-1,k])
										
									if _auxCube[_i,_j,_k+1]:
										_neighborVal.append([i,j,k+1])
											
									if _auxCube[_i,_j,_k-1]:
										_neighborVal.append([i,j,k-1])
											
									if _auxCube[_i+1,_j+1,_k]:
										_neighborVal.append([i+1,j+1,k])
											
									if _auxCube[_i+1,_j-1,_k]:
										_neighborVal.append([i+1,j-1,k])
											
									if _auxCube[_i-1,_j+1,_k]:
										_neighborVal.append([i-1,j+1,k])
											
									if _auxCube[_i-1,_j-1,_k]:
										_neighborVal.append([i-1,j-1,k])
											
									if _auxCube[_i+1,_j,_k+1]:
										_neighborVal.append([i+1,j,k+1])
										
									if _auxCube[_i-1,_j,_k+1]:
										_neighborVal.append([i-1,j,k+1])
											
									if _auxCube[_i,_j+1,_k+1]:
										_neighborVal.append([i,j+1,k+1])
											
									if _auxCube[_i,_j-1,_k+1]:
										_neighborVal.append([i,j-1,k+1])
											
									if _auxCube[_i+1,_j,_k-1]:
										_neighborVal.append([i+1,j,k-1])
											
									if _auxCube[_i-1,_j,_k-1]:
										_neighborVal.append([i-1,j,k-1])
											
									if _auxCube[_i,_j+1,_k-1]:
										_neighborVal.append([i,j+1,k-1])
											
									if _auxCube[_i,_j-1,_k-1]:
										_neighborVal.append([i,j-1,k-1])
									
									if _auxCube[_i+1,_j+1,_k+1]:
										_neighborVal.append([i+1,j+1,k+1])
											
									if _auxCube[_i+1,_j-1,_k+1]:
										_neighborVal.append([i+1,j-1,k+1])
									
									if _auxCube[_i-1,_j+1,_k+1]:
										_neighborVal.append([i-1,j+1,k+1])
									
									if _auxCube[_i-1,_j-1,_k+1]:
										_neighborVal.append([i-1,j-1,k+1])
								
									if _auxCube[_i+1,_j+1,_k-1]:
										_neighborVal.append([i+1,j+1,k-1])
											
									if _auxCube[_i+1,_j-1,_k-1]:
										_neighborVal.append([i+1,j-1,k-1])
									
									if _auxCube[_i-1,_j+1,_k-1]:
										_neighborVal.append([i-1,j+1,k-1])
											
									if _auxCube[_i-1,_j-1,_k-1]:
										_neighborVal.append([i-1,j-1,k-1])
									
									_loopCounter += 1
										
								i = _origiVal
								j = _origjVal
								k = _origkVal

								if self._writeNeighborInformation:
									
									_neighborVal.append([i, j, k])
									_neighborVal = np.array(_neighborVal)
									
									fw = open('NeighborInformation.txt', 'a')
									fw.write(str(_structVal) + ' ' + str(min(_neighborVal[:, 0])) + ' ' + str(max(_neighborVal[:, 0])) + ' ' + str(min(_neighborVal[:, 1])) + ' ' + str(max(_neighborVal[:, 1])) + ' ' + str(min(_neighborVal[:, 2])) + ' ' + str(max(_neighborVal[:, 2])) + '\n')
									fw.close()

		#---------------------------------------------------------------------#

		# Restore back to original grid

		_structValuedGrid = _structValuedGrid[:self.xlen, :self.ylen, :self.zlen]

		#---------------------------------------------------------------------#

		# Write out all data
									
		_structValuedGrid = _structValuedGrid.ravel()				

		u, counts = np.unique(_structValuedGrid, return_counts = True)
		
		if self.verbose:
			print('Unique structure identifiers:', u)
			print('Counts for the unique structures:', counts)

		countsall = copy.deepcopy(counts)
		countsall.sort()
		if self.verbose:
			print('Index of the biggest structure(s):', np.where(np.in1d(counts, countsall[::-1][1])))
		Vmax = countsall[::-1][1]
		if self.verbose:
			print('Rearranged counts of structures:', countsall[::-1][:10])
		Vall = sum(countsall[::-1][1:])
		if self.verbose:
			print('Sum of counts of all structures: ', Vall)

		if self._writePercolationData:
			
			fw = open('Percolation_threshold.txt', 'a')
			fw.write(str(self._threshVal) + ' ' + str(Vmax) + ' ' + str(Vall) + '\n')
			fw.close()

		if self.verbose:
			print('Total time:', time.time() - start_time)
		
		return _structValuedGrid
