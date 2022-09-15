#! /bin/sh

pip install -e .
find _skbuild/linux-*/cmake-install/qiskit_aer/backends -name "controller_wrappers*.so" -exec cp {} `pwd`/qiskit_aer/backends/ \;
find _skbuild/linux-*/cmake-install/qiskit_aer/pulse/controllers -name "pulse_utils*.so" -exec cp {} `pwd`/qiskit_aer/pulse/controllers/ \;
rm -rf `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
ln -s `pwd`/qiskit_aer `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
