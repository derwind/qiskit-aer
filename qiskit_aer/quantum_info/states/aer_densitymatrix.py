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
import os ###
import inspect ###
import copy
import numpy as np

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.quantum_info.states import DensityMatrix

from qiskit_aer import AerSimulator
from .aer_statevector import AerStatevector
from .aer_state import AerState
from ...backends.aerbackend import AerError

def getframeinfo(stackIndex=2):
    """
    @see http://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
    @return frameInfo
    """

    stack = inspect.stack()
    if stackIndex >= len(stack):
        return None

    callerframerecord = stack[stackIndex]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    return info

def dbg_print(*msg):
    info = getframeinfo()
    filename = info.filename.split(os.sep)[-1]
    print(f'[{filename}:{info.lineno} ({info.function})]', *msg)

class AerDensityMatrix(DensityMatrix):
    """AerDensityMatrix class
    This class inherits :class:`DensityMatrix`.
    """

    def __init__(self, data, dims=None, **configs):
        """
        Args:
            configs (kwargs): configurations of :class:`AerDensityMatrix`. `_aer_state` and `method` are valid.
        Raises:
            AerError: if input data is not valid.
        Additional Information:
            The ``dims`` kwarg is used to ``AerDensityMatrix`` constructor.
        """
        if '_aer_state' in configs:
            self._aer_state = configs.pop('_aer_state')
        else:
            #if 'method' not in configs:
            #    configs['method'] = 'densitymatrix'
            #elif configs['method'] not in ('densitymatrix'):
            #    method = configs['method']
            #    raise AerError(f'Method {method} is not supported')
            if isinstance(data, (QuantumCircuit, Instruction)):
                data, aer_state = AerDensityMatrix._from_instruction(data, None, configs)
            elif isinstance(data, list):
                data, aer_state = AerDensityMatrix._from_ndarray(data, configs)
            elif isinstance(data, np.ndarray):
                data, aer_state = AerDensityMatrix._from_ndarray(data, configs)
            elif isinstance(data, AerDensityMatrix):
                aer_state = data._aer_state
                if dims is None:
                    dims = data._op_shape._dims_l
                data = data._data.copy()
            elif isinstance(data, AerStatevector):
                data, aer_state = AerDensityMatrix._from_ndarray(data.data, configs)
            else:
                raise AerError(f'Input data is not supported: type={data.__class__}, data={data}')

            self._aer_state = aer_state
            dbg_print(self._aer_state.configuration())

        super().__init__(data, dims=dims)

        self._result = None
        self._configs = configs

    def __copy__(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, _memo=None):
        ret = AerDensityMatrix(self._data.copy(), **self._configs)
        ret._op_shape = copy.deepcopy(self._op_shape)
        ret._rng_generator = copy.deepcopy(self._rng_generator)
        return ret

    @staticmethod
    def _from_ndarray(init_data, configs):
        aer_state = AerState(method='density_matrix')

        options = AerSimulator._default_options()
        for config_key, config_value in configs.items():
            if options.get(config_key):
                aer_state.configure(config_key, config_value)

        if len(init_data) == 0:
            raise AerError('initial data must be larger than 0')

        num_qubits = int(np.log2(len(init_data)))

        aer_state.allocate_qubits(num_qubits)
        aer_state.initialize(data=init_data)

        return aer_state.move_to_ndarray(), aer_state

    @classmethod
    def from_instruction(cls, instruction):
        return AerDensityMatrix(instruction)

    @staticmethod
    def _from_instruction(inst, init_data, configs):
        #aer_state = AerState(method='density_matrix')
        aer_state = AerState()

        for config_key, config_value in configs.items():
            aer_state.configure(config_key, config_value)

        aer_state.allocate_qubits(inst.num_qubits)
        #num_qubits = inst.num_qubits

        if init_data is not None:
            aer_state.initialize(data=init_data, copy=True)
        else:
            aer_state.initialize()

        if isinstance(inst, QuantumCircuit) and inst.global_phase != 0:
            aer_state.apply_global_phase(inst.global_phase)

        #if isinstance(inst, QuantumCircuit):
        #    AerDensityMatrix._aer_evolve_circuit(aer_state, inst, range(num_qubits))
        #else:
        #    AerDensityMatrix._aer_evolve_instruction(aer_state, inst, range(num_qubits))

        return aer_state.move_to_ndarray(), aer_state
