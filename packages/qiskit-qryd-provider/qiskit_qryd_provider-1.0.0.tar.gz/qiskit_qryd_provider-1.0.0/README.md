# Qiskit QRyd Provider

![Supported Python versions](https://img.shields.io/pypi/pyversions/qiskit_qryd_provider.svg?color=blue)
[![Package version on PyPI](https://img.shields.io/pypi/v/qiskit_qryd_provider.svg?color=blue)](https://pypi.org/project/qiskit_qryd_provider/)
[![Documentation](https://img.shields.io/badge/docs-Sphinx-blue.svg)](https://thequantumlaend.de/docs/)
[![License](https://img.shields.io/pypi/l/qiskit_qryd_provider.svg?color=green)](https://www.apache.org/licenses/LICENSE-2.0)

This Python library contains a provider for the [Qiskit](https://qiskit.org) quantum computing framework. The provider allows for accessing the GPU-based emulator and the future Rydberg quantum computer of the [QRydDemo](https://thequantumlaend.de/qryddemo/) consortium.

Interactive tutorials can be found on QRydDemo's [Jupyter server](https://thequantumlaend.de/frontend).

## Installation

The provider can be installed via [pip](https://pip.pypa.io/) from
[PyPI](https://pypi.org/project/qiskit_qryd_provider/):

```bash
pip install qiskit-qryd-provider
```

## Basic Usage

To use the provider, a QRydDemo API token is required. The token can be obtained via our [online registration form](https://thequantumlaend.de/frontend/signup_form.php). You can use the token to initialize the provider:

```python
from qiskit_qryd_provider import QRydProvider

provider = QRydProvider("MY_TOKEN")
```

Afterwards, you can choose a backend. Different backends are available that are capable of running ideal simulations of quantum circuits. An inclusion of noise models is planned for the future. You can either choose a backend emulating 30 qubits arranged in a 5x6 square lattice with nearest-neighbor connectivity

```python
backend = provider.get_backend("qryd_emulator$square")
```

or a backend emulating 30 qubits arranged in a triangle lattice with nearest-neighbor connectivity

```python
backend = provider.get_backend("qryd_emulator$triangle")
```

If you use these backends, the compilation of quantum circuits happens on our servers. The circuits are compiled to comply with the native gate set and connectivity of the Rydberg platform, using a decomposer developed by [HQS Quantum Simulations](https://quantumsimulations.de/).

After selecting a backend, you can run a circuit on the backend, using the `transpile` function followed by `backend.run`:

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
job = backend.run(transpile(qc, backend), shots=200)
print(job.result().get_counts())
```

Alternatively, you can use the `BackendSampler` primitive:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSampler

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
job = BackendSampler(backend).run(qc, shots=200)
print(job.result().quasi_dists[0])
```

## Expert Options

The provider adds the phase-shifted controlled-Z gate ([PCZGate](https://thequantumlaend.de/docs/gates.html#qiskit_qryd_provider.PCZGate)) and the phase-shifted controlled-phase gate ([PCPGate](https://thequantumlaend.de/docs/gates.html#qiskit_qryd_provider.PCPGate)) to Qiskit. These gates equal the controlled-Z/phase gates up to single-qubit phase gates. The gates can be realized by the Rydberg platform in multiple ways [[1](https://doi.org/10.1103/PhysRevLett.123.170503), [2](https://doi.org/10.1103/PhysRevResearch.4.033019), [3](https://doi.org/10.22331/q-2022-05-13-712)]. The value of the phase shift of the PCZGate can be modified before using the backend via:

```python
from qiskit_qryd_provider import PCZGate

PCZGate.set_theta(1.234)
```

## License

The Qiskit QRyd Provider is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
