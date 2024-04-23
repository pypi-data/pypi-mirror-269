from typing import List

import requests
from qiskit.providers import ProviderV1 as Provider
from qiskit.providers import QiskitBackendNotFoundError
from qiskit.providers.providerutils import filter_backends

from qiskit_qryd_provider.qryd_backend import NoisyEmulatorTriangle
from qiskit_qryd_provider.qryd_backend import QRydBackend
from qiskit_qryd_provider.qryd_backend import QRydEmulatorSquare
from qiskit_qryd_provider.qryd_backend import QRydEmulatorTriangle


class QRydProvider(Provider):
    """Provider for backends from the `QRydDemo`_ consortium.

    .. _QRydDemo: https://thequantumlaend.de/qryddemo/

    This class provides backends for accessing QRydDemo's cloud infrastructure with
    Qiskit. To access the infrastructure, a valid API token is required. The token can
    be obtained via our `online registration form
    <https://thequantumlaend.de/frontend/signup_form.php>`_.

    Different backends are available that are capable of running ideal simulations of
    quantum circuits on the GPU-based emulator of the QRydDemo consortium. An inclusion
    of noise models is planned for the future. Currently, the following backends are
    provided:

    * :class:`~qiskit_qryd_provider.QRydEmulatorSquare`:
      emulator of 30 ideal qubits arranged in a 5x6 square lattice with
      nearest-neighbor connectivity, quantum circuits are compiled to the gate set of
      the Rydberg platform on our servers after submitting the circuits to QRydDemo's
      infrastructure.
    * :class:`~qiskit_qryd_provider.QRydEmulatorTriangle`:
      emulator of 30 ideal qubits arranged in a triangle lattice with
      nearest-neighbor connectivity, quantum circuits are compiled to the gate set of
      the Rydberg platform on our servers after submitting the circuits to QRydDemo's
      infrastructure.

    In addition, the following backends are provided that serve special purposes:

    * :class:`~qiskit_qryd_provider.NoisyEmulatorTriangle`:
      emulator of up to 16 qubits arranged in a triangle lattice with
      nearest-neighbor connectivity and simple noise models,
      useful for studying quantum error correction codes. Under development.

    Typical usage example:

    .. testcode::

        from qiskit_qryd_provider import QRydProvider
        import os

        provider = QRydProvider(os.getenv("QRYD_API_TOKEN"))
        backend = provider.get_backend("qryd_emulator$square")

    """

    url_base = "https://api.qryddemo.itp3.uni-stuttgart.de/v5_1/jobs"
    """URL to the `web API
    <https://api.qryddemo.itp3.uni-stuttgart.de/docs>`_ endpoint for submitting
    simulation jobs to QRydDemo's cloud emulator."""

    def __init__(self, token: str, dev: bool = False) -> None:  # TODO
        """Initialize the provider.

        Args:
            token: The QrydDemo Api token that can be obtained via our `online
                registration form
                <https://thequantumlaend.de/frontend/signup_form.php>`__.
            dev: Whether to use the development version of the API.

        """
        super().__init__()
        self.session = requests.Session()
        if dev:
            self.session.headers.update({"X-API-KEY": token, "X-DEV": "?1"})
        else:
            self.session.headers.update({"X-API-KEY": token})

    def get_backend(self, name: str = None, **kwargs) -> QRydBackend:
        """Return a single backend matching the specified filtering.

        Args:
            name: Name of the backend.
            **kwargs: Dict used for filtering.

        Returns:
            A backend matching the filtering.

        Raises:
            qiskit.providers.QiskitBackendNotFoundError: If no backend could be found or
                more than one backend matches the filtering criteria.

        .. # noqa: DAR401
        .. # noqa: DAR402

        """
        backends = self.backends(name, **kwargs)
        if len(backends) > 1:
            raise QiskitBackendNotFoundError("More than one backend matches criteria.")
        if not backends:
            raise QiskitBackendNotFoundError("No backend matches criteria.")

        return backends[0]

    def backends(self, name: str = None, **kwargs) -> List[QRydBackend]:
        """Return a list of backends matching the specified filtering.

        Args:
            name: Name of the backend.
            **kwargs: Dict used for filtering.

        Returns:
            A list of backends that match the filtering criteria.

        """
        backends = [
            QRydEmulatorSquare(provider=self),
            QRydEmulatorTriangle(provider=self),
            NoisyEmulatorTriangle(provider=self),
        ]  # type: List[QRydBackend]
        if name:
            backends = [backend for backend in backends if backend.name == name]
        return filter_backends(backends, **kwargs)
