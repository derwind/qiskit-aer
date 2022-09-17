# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019, 2020, 2021, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
DensityMatrix quantum state class.
"""
import copy
import numpy as np

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.quantum_info.states import DensityMatrix

from qiskit_aer import AerSimulator
from .aer_state import AerState
from ...backends.aerbackend import AerError

class AerDensityMatrix(DensityMatrix):

    def __init__(self, data, dims=None):
        pass

    def __copy__(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, _memo=None):
        ret = AerDensityMatrix(self._data.copy(), **self._configs)
        ret._op_shape = copy.deepcopy(self._op_shape)
        ret._rng_generator = copy.deepcopy(self._rng_generator)
        return ret
