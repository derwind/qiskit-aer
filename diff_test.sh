#! /bin/sh

cp test/terra/states/test_aer_densitymatrix.py test/terra/states/test_aer_densitymatrix_.py
perl -pi -e 's/AerDensityMatrix/DensityMatrix' test/terra/states/test_aer_densitymatrix_.py
diff -u test/terra/states/test_aer_densitymatrix_.py ../qiskit-terra/test/python/quantum_info/states/test_densitymatrix.py
