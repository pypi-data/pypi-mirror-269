# Script to run GenerateClump_Euclidean_3D (Extended Euclidean method)
# 2021 © V. Angelidakis, S. Nadimi, M. Otsubo, S. Utili.

# 2021 MATLAB implementation by V. Angelidakis <v.angelidakis@qub.ac>
# 2024 Translated from MATLAB to Python by U.A. Canbolat <utku.canbolat@fau.de>

import sys
sys.path.append('/home/vas/Desktop/Utku_Code_Review/CLUMP_Python/')

from CLUMP.GenerateClump_Euclidean_3D import GenerateClump_Euclidean_3D
import sys
sys.path.append('../')

# Load particle shape from stl file
inputGeom = 'ParticleGeometries/Human_femur.stl'
N = 200
rMin = 0
div = 102
overlap = 0.0
output = 'EU_Human_femur.txt'
outputVTK = 'EU_Human_femur.vtk'
visualise = True
rMax_ratio = 0.3 # Parameter to trigger the Extended Euclidean method

mesh,clump = GenerateClump_Euclidean_3D(inputGeom=inputGeom, N=N, rMin=rMin, div=div, overlap=overlap, output=output, outputVTK=outputVTK, visualise=visualise, rMax_ratio=rMax_ratio)

print('Total number of spheres: '+ str(clump.numSpheres))
