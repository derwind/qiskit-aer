# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
QasmSimulator Integration Tests
"""

import unittest
from test.terra import common
from test.terra.backends.qasm_simulator.qasm_method import QasmMethodTests
from test.terra.backends.qasm_simulator.qasm_measure import QasmMeasureTests
from test.terra.backends.qasm_simulator.qasm_reset import QasmResetTests
from test.terra.backends.qasm_simulator.qasm_conditional import QasmConditionalGateTests
from test.terra.backends.qasm_simulator.qasm_cliffords import QasmCliffordTests
from test.terra.backends.qasm_simulator.qasm_algorithms import QasmAlgorithmTests


class TestQasmStabilizerSimulator(common.QiskitAerTestCase,
                                  QasmMethodTests,
                                  QasmMeasureTests,
                                  QasmResetTests,
                                  QasmConditionalGateTests,
                                  QasmCliffordTests,
                                  QasmAlgorithmTests):
    """QasmSimulator stabilizer method tests."""

    BACKEND_OPTS = {"method": "stabilizer"}


if __name__ == '__main__':
    unittest.main()
