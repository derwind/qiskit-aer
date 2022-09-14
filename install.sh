#! /bin/sh

pip install -U dist/qiskit_aer*.whl
rm -rf `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
ln -s `python -c "import site; print (site.getsitepackages()[0])"`/qiskit_aer `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
