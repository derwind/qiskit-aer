#! /bin/sh

python ./setup.py bdist_wheel -- DCMAKE_CXX_COMPILER=g++-7 -DAER_THRUST_BACKEND=OMP -- -j8
