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
from qiskit.exceptions import QiskitError
from qiskit.quantum_info.states import DensityMatrix
from qiskit.quantum_info.operators.predicates import is_hermitian_matrix

from qiskit_aer import AerSimulator
from .aer_statevector import AerStatevector
from .aer_state import AerState
from ...backends.aerbackend import AerError


class AerDensityMatrix(DensityMatrix):
    """AerDensityMatrix class
    This class inherits :class:`DensityMatrix`.
    """

    def __init__(self, data, dims=None, **configs):
        """
        Args:
            data (np.array or list or AerStatevector or QuantumCircuit or
                  qiskit.circuit.Instruction):
                Data from which the densitymatrix can be constructed. This can be either a complex
                vector, another densitymatrix or statevector or a ``QuantumCircuit`` or
                ``Instruction`` (``Operator`` is not supportted in the current implementation).
                If the data is a circuit or instruction, the densitymatrix is constructed by
                assuming that all qubits are initialized to the zero state.
            dims (int or tuple or list): Optional. The subsystem dimension of
                                         the state (See additional information).
            configs (kwargs): configurations of :class:`AerDensityMatrix`. `_aer_state` and `method`
            are valid.
        Raises:
            AerError: if input data is not valid.
        Additional Information:
            The ``dims`` kwarg is used to ``AerDensityMatrix`` constructor.
        """
        if '_aer_state' in configs:
            self._aer_state = configs.pop('_aer_state')
        else:
            if 'method' not in configs:
                configs['method'] = 'density_matrix'
            elif configs['method'] not in ('density_matrix'):
                method = configs['method']
                raise AerError(f'Method {method} is not supported')
            if isinstance(data, (QuantumCircuit, Instruction)):
                data, aer_state = AerDensityMatrix._from_instruction(data, None, configs)
            elif isinstance(data, list):
                data, aer_state = AerDensityMatrix._from_ndarray(np.array(data, dtype=complex),
                                                                 configs)
            elif isinstance(data, np.ndarray):
                data, aer_state = AerDensityMatrix._from_ndarray(data, configs)
            elif isinstance(data, AerDensityMatrix):
                aer_state = data._aer_state
                if dims is None:
                    dims = data._op_shape._dims_l
                data = data._data.copy()
            elif hasattr(data, 'to_operator'):
                # If the data object has a 'to_operator' attribute this is given
                # higher preference than the 'to_matrix' method for initializing
                # an Operator object.
                op = data.to_operator()
                data, aer_state = AerDensityMatrix._from_ndarray(op.data, configs)
                if dims is None:
                    dims = op.output_dims()
            elif hasattr(data, 'to_matrix'):
                # If no 'to_operator' attribute exists we next look for a
                # 'to_matrix' attribute to a matrix that will be cast into
                # a complex numpy matrix.
                data, aer_state = AerDensityMatrix._from_ndarray(
                    np.asarray(data.to_matrix(), dtype=complex), configs)
            else:
                raise AerError(f'Input data is not supported: type={data.__class__}, data={data}')

            self._aer_state = aer_state

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
        aer_state = AerState(method='density_matrix')

        for config_key, config_value in configs.items():
            aer_state.configure(config_key, config_value)

        aer_state.allocate_qubits(inst.num_qubits)
        num_qubits = inst.num_qubits

        if init_data is not None:
            aer_state.initialize(data=init_data, copy=True)
        else:
            aer_state.initialize()

        if isinstance(inst, QuantumCircuit) and inst.global_phase != 0:
            aer_state.apply_global_phase(inst.global_phase)

        if isinstance(inst, QuantumCircuit):
            AerStatevector._aer_evolve_circuit(aer_state, inst, range(num_qubits))
        else:
            AerStatevector._aer_evolve_instruction(aer_state, inst, range(num_qubits))

        return aer_state.move_to_ndarray(), aer_state

    @classmethod
    def from_label(cls, label):
        r"""Return a tensor product of Pauli X,Y,Z eigenstates.
        .. list-table:: Single-qubit state labels
           :header-rows: 1
           * - Label
             - Statevector
           * - ``"0"``
             - :math:`\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}`
           * - ``"1"``
             - :math:`\begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}`
           * - ``"+"``
             - :math:`\frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}`
           * - ``"-"``
             - :math:`\frac{1}{2}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}`
           * - ``"r"``
             - :math:`\frac{1}{2}\begin{pmatrix} 1 & -i \\ i & 1 \end{pmatrix}`
           * - ``"l"``
             - :math:`\frac{1}{2}\begin{pmatrix} 1 & i \\ -i & 1 \end{pmatrix}`
        Args:
            label (string): a eigenstate string ket label (see table for
                            allowed values).
        Returns:
            Statevector: The N-qubit basis state density matrix.
        Raises:
            QiskitError: if the label contains invalid characters, or the length
                         of the label is larger than an explicitly specified num_qubits.
        """
        return AerDensityMatrix(AerStatevector.from_label(label))

    @staticmethod
    def from_int(i, dims):
        """Return a computational basis state density matrix.
        Args:
            i (int): the basis state element.
            dims (int or tuple or list): The subsystem dimensions of the statevector
                                         (See additional information).
        Returns:
            DensityMatrix: The computational basis state :math:`|i\\rangle\\!\\langle i|`.
        Additional Information:
            The ``dims`` kwarg can be an integer or an iterable of integers.
            * ``Iterable`` -- the subsystem dimensions are the values in the list
              with the total number of subsystems given by the length of the list.
            * ``Int`` -- the integer specifies the total dimension of the
              state. If it is a power of two the state will be initialized
              as an N-qubit state. If it is not a power of  two the state
              will have a single d-dimensional subsystem.
        """
        size = np.product(dims)
        state = np.zeros((size, size), dtype=complex)
        state[i, i] = 1.0
        return AerDensityMatrix(state, dims=dims)

    def to_statevector(self, atol=None, rtol=None):
        """Return a statevector from a pure density matrix.
        Args:
            atol (float): Absolute tolerance for checking operation validity.
            rtol (float): Relative tolerance for checking operation validity.
        Returns:
            AerStatevector: The pure density matrix's corresponding statevector.
                Corresponds to the eigenvector of the only non-zero eigenvalue.
        Raises:
            QiskitError: if the state is not pure.
        """
        if atol is None:
            atol = self.atol
        if rtol is None:
            rtol = self.rtol

        if not is_hermitian_matrix(self.data, atol=atol, rtol=rtol):
            raise QiskitError('Not a valid density matrix (non-hermitian).')

        evals, evecs = np.linalg.eig(self.data)

        nonzero_evals = evals[abs(evals) > atol]
        if len(nonzero_evals) != 1 or not np.isclose(nonzero_evals[0], 1, atol=atol, rtol=rtol):
            raise QiskitError('Density matrix is not a pure state')

        psi = evecs[:, np.argmax(evals)]  # eigenvectors returned in columns.
        # XXX: The internal representation of psi affects statevector's representatio,
        # so change the ordering of psi to C ordering.
        return AerStatevector(np.ascontiguousarray(psi))
