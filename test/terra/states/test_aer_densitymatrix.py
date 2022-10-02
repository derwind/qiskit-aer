# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
Integration Tests for AerDensityMatrix
"""

import os
import sys
import unittest
from math import pi
import numpy as np
import logging
from itertools import permutations
from ddt import ddt, data
from numpy.testing import assert_allclose

from qiskit import transpile
from qiskit.exceptions import QiskitError
from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.providers.basicaer import QasmSimulatorPy
from qiskit.quantum_info.random import random_unitary, random_statevector, random_pauli
from qiskit.quantum_info.states import Statevector
from qiskit.circuit.library import QuantumVolume
from qiskit.providers.aer import AerSimulator
from qiskit.quantum_info.operators.operator import Operator
from qiskit.quantum_info.operators.symplectic import Pauli, SparsePauliOp
from qiskit.quantum_info.operators.predicates import matrix_equal
from qiskit.visualization.state_visualization import numbers_to_latex_terms, state_to_latex
from qiskit.circuit.library import QFT, HGate
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from test.terra import common
from qiskit_aer.aererror import AerError
from qiskit_aer.quantum_info.states import AerDensityMatrix


logger = logging.getLogger(__name__)

@ddt
class TestAerDensityMatrix(common.QiskitAerTestCase):
    """AerDensityMatrix tests"""

    @classmethod
    def rand_vec(cls, n, normalize=False):
        """Return complex vector or statevector"""
        seed = np.random.randint(0, np.iinfo(np.int32).max)
        logger.debug("rand_vec default_rng seeded with seed=%s", seed)
        rng = np.random.default_rng(seed)
        vec = rng.random(n) + 1j * rng.random(n)
        if normalize:
            vec /= np.sqrt(np.dot(vec, np.conj(vec)))
        return vec

    @classmethod
    def rand_rho(cls, n):
        """Return random pure state density matrix"""
        rho = cls.rand_vec(n, normalize=True)
        return np.outer(rho, np.conjugate(rho))

    def test_init_array_qubit(self):
        """Test subsystem initialization from N-qubit array."""
        # Test automatic inference of qubit subsystems
        rho = self.rand_rho(8)
        for dims in [None, 8]:
            state = AerDensityMatrix(rho, dims=dims)
            assert_allclose(state.data, rho)
            self.assertEqual(state.dim, 8)
            self.assertEqual(state.dims(), (2, 2, 2))
            self.assertEqual(state.num_qubits, 3)

if __name__ == '__main__':
    unittest.main()
