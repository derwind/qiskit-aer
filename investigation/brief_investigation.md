# [Qiskit/qiskit-aer](https://github.com/Qiskit/qiskit-aer)

> Qiskit is made up of elements that each work together to enable quantum computing. This element is **Aer**, which provides high-performance quantum computing simulators with realistic noise models.

## How to install

[Install from Source](https://github.com/Qiskit/qiskit-aer/blob/main/CONTRIBUTING.md#install-from-source)

### Preparetion

```sh
$ sudo apt install build-essential
$ apt-get install git
$ git clone https://github.com/Qiskit/qiskit-aer
$ cd qiskit-aer
$ pip install -r requirements-dev.txt
$ pip install conan
```

### Build

```sh
$ python ./setup.py bdist_wheel
```

It takes a little time because the shared library build runs.

## Install

### Uninstall previous version

```sh
$ pip uninstal qiskit-aer
```

### Install newer version

Recommended: (It will be installed, although an error message will appear in terms of dependencies with other modules.)

```sh
$ pip install -U dist/qiskit_aer*.whl
$ find _skbuild/linux-*/cmake-install/qiskit_aer/backends -name "controller_wrappers*.so" -exec cp {} `python -c "import site; print (site.getsitepackages()[0])"`/qiskit_aer/backends/ \;
$ ln -s `python -c "import site; print (site.getsitepackages()[0])"`/qiskit_aer `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
```

or

```sh
$ python setup.py install
...
```

or

```sh
$ python setup.py install -e .
$ find _skbuild/linux-*/cmake-install/qiskit_aer/backends -name "controller_wrappers*.so" -exec cp {} `pwd`/qiskit_aer/backends/ \;
$ find _skbuild/linux-*/cmake-install/qiskit_aer/pulse/controllers -name "pulse_utils*.so" -exec cp {} `pwd`/qiskit_aer/pulse/controllers/ \;
$ ln -s `pwd`/qiskit_aer `python -c "import site; print (site.getsitepackages()[0])"`/qiskit/providers/aer
```

## ~~Latest code (obsoleted)~~

~~You can get the latest code from PR as a branch by doing the following:~~

```sh
$ git fetch origin pull/1590/head:add_aer_statevector
$ git checkout add_aer_statevector
```

## Sample Codes

```python
>>> from numpy import sqrt
>>> from qiskit.providers.aer.quantum_info import AerStatevector
>>> sv=AerStatevector([1/sqrt(2), 0, 0, -1/sqrt(2)])
>>> sv.draw(output='latex')
```

## Sequence of inilialization

![](images/qiskit-aer-StateVector_Initialization.svg)

## State transition of AerState

![](images/qiskit-aer-AerState_state_transition.svg)

## Overriden or added new methods in AerStatevector

- Overriden
    - `conjugate` (of Statevector)
    - `sample_memory` (of QuantumState)
- Added
    - `__copy__`
    - `__deepcopy__`
    - `__init__`
    - `_last_result`
    - `from_instruction` (@classmethod)
    - `from_label` (@classmethod)
    - `metadata`

### Affected existing methods

- `conjugate`
    - `expectation_value` (of Statevector)
- `sample_memory`
    - `sample_counts` (of QuantumState/Statevector)
