# Script to run GenerateClump_Euclidean_3D
# 2021 © V. Angelidakis, S. Nadimi, M. Otsubo, S. Utili.

# 2021 MATLAB implementation by V. Angelidakis <v.angelidakis@qub.ac>
# 2024 Translated from MATLAB to Python by U.A. Canbolat <utku.canbolat@fau.de>

import sys

from CLUMP.GenerateClump_Euclidean_3D import GenerateClump_Euclidean_3D
import sys
sys.path.append('../../')

# Load particle shape from stl file
inputGeom = 'ParticleGeometries/Hexahedron.stl'
N = 21
rMin = 0
div = 102
overlap = 0.6
output = 'EU_Hexahedron.txt'
outputVTK = 'EU_Hexahedron.vtk'
visualise = True

mesh,clump = GenerateClump_Euclidean_3D(inputGeom=inputGeom, N=N, rMin=rMin, div=div, overlap=overlap, output=output, outputVTK=outputVTK, visualise=visualise)

print('Total number of spheres: '+ str(clump.numSpheres))
