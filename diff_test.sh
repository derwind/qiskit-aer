#! /bin/sh

cp test/terra/states/test_aer_densitymatrix.py test/terra/states/test_aer_densitymatrix_.py
perl -pi -e 's/AerDensityMatrix/DensityMatrix/g; s/AerStatevector/Statevector/g' test/terra/states/test_aer_densitymatrix_.py
diff -u ../qiskit-terra/test/python/quantum_info/states/test_densitymatrix.py test/terra/states/test_aer_densitymatrix_.py
