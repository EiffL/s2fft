import numpy as np
from typing import Tuple


def f_shape(L: int, N: int, sampling: str = "mw") -> Tuple[int, int, int]:
    r"""Computes the pixel-space sampling shape for signal on the rotation group
    :math:`SO(3)`.

    Importantly, the convention we are using for storage is :math:`[\beta, \alpha,
    \gamma]` in order to simplify indexing for internal use. For a given :math:`\gamma`
    we thus recover a signal on the sphere indexed by :math:`[\theta, \phi]`, i.e. we
    associate :math:`\beta` with :math:`\theta` and :math:`\alpha` with :math:`\phi`.

    Args:
        L (int): Harmonic band-limit.

        N (int): Directional band-limit.

        sampling (str, optional): Sampling scheme.  Supported sampling schemes include
            {"mw", "mwss", "dh"}.  Defaults to "mw".

    Raises:
        ValueError: Unknown sampling scheme.

    Returns:
        Tuple[int,int,int]: Shape of pixel-space sampling of rotation group
        :math:`SO(3)`.
    """
    if sampling in ["mw", "mwss", "dh"]:

        return _nbeta(L, sampling), _nalpha(L, sampling), _ngamma(N)

    else:

        raise ValueError(f"Sampling scheme sampling={sampling} not supported")


def flmn_shape(L: int, N: int) -> Tuple[int, int, int]:
    r"""Computes the shape of Wigner coefficients for signal on the rotation group
    :math:`SO(3)`.

    TODO: Add support for compact storage etc.

    Args:
        L (int): Harmonic band-limit.

        N (int): Directional band-limit.

    Returns:
        Tuple[int,int,int]: Shape of Wigner space sampling of rotation group
            :math:`SO(3)`.
    """
    return L, 2 * L - 1, 2 * N - 1


def flmn_shape_1d(L: int, N: int) -> int:
    r"""Computes the number of non-zero Wigner coefficients.

    TODO: Add support for compact storage etc.

    Args:
        L (int): Harmonic band-limit.

        N (int): Directional band-limit.

    Returns:
        int: Total number of non-zero Wigner coefficients.
    """
    return (2 * N - 1) * L * L


def _nalpha(L: int, sampling: str = "mw") -> int:
    r"""Computes the number of :math:`\alpha` samples.

    Args:
        L (int): Harmonic band-limit.

        sampling (str, optional): Sampling scheme.  Supported sampling schemes include
            {"mw", "mwss", "dh"}.  Defaults to "mw".

    Raises:
        ValueError: Unknown sampling scheme.

    Returns:
        int: Number of :math:`\alpha` samples.
    """
    if sampling.lower() in ["mw", "dh"]:

        return 2 * L - 1

    elif sampling.lower() == "mwss":

        return 2 * L

    else:

        raise ValueError(f"Sampling scheme sampling={sampling} not supported")

    return 1


def _nbeta(L: int, sampling: str = "mw") -> int:
    r"""Computes the number of :math:`\beta` samples.

    Args:
        L (int): Harmonic band-limit.

        sampling (str, optional): Sampling scheme.  Supported sampling schemes include
            {"mw", "mwss", "dh"}.  Defaults to "mw".

    Raises:
        ValueError: Unknown sampling scheme.

    Returns:
        int: Number of :math:`\beta` samples.
    """
    if sampling.lower() == "mw":

        return L

    elif sampling.lower() == "mwss":

        return L + 1

    elif sampling.lower() == "dh":

        return 2 * L

    else:

        raise ValueError(f"Sampling scheme sampling={sampling} not supported")

    return 1


def _ngamma(N: int) -> int:
    r"""Computes the number of :math:`\gamma` samples.

    Args:
        N (int): Directional band-limit.

    Returns:
        int: Number of :math:`\gamma` samples, by default :math:`2N-1`.
    """
    return 2 * N - 1


def elmn2ind(el: int, m: int, n: int, L: int, N: int = 1) -> int:
    """Convert from Wigner space 3D indexing of :math:`(\ell,m, n)` to 1D index.

    Args:
        el (int): Harmonic degree :math:`\ell`.

        m (int): Harmonic order :math:`m`.

        n (int): Directional order :math:`n`.

        L (int): Harmonic band-limit.

        N (int, optional): Directional band-limit. Defaults to 1.

    Returns:
        int: Corresponding 1D index in Wigner space.
    """
    n_offset = (N - 1 + n) * L * L
    el_offset = el * el
    return n_offset + el_offset + el + m


def flmn_3d_to_1d(flmn_3d: np.ndarray, L: int, N: int = 1) -> np.ndarray:
    r"""Convert from 3D indexed Wigner coefficients to 1D indexed coefficients.

    Args:
        flm_3d (np.ndarray): 3D indexed Wigner coefficients, index order
            :math:`[\ell, m, n]`.

        L (int): Harmonic band-limit.

        N (int, optional): Directional band-limit. Defaults to 1.

    Raises:
        ValueError: `flmn` is already 1D indexed.

        ValueError: `flmn` is not 3D.

    Returns:
        np.ndarray: 1D indexed Wigner coefficients, C flatten index priority :math:`n, \ell, m`.
    """
    flmn_1d = np.zeros(flmn_shape_1d(L, N), dtype=np.complex128)

    if len(flmn_3d.shape) == 1:
        raise ValueError(f"flmn is already 1D indexed")
    elif len(flmn_3d.shape) != 3:
        raise ValueError(
            f"Cannot convert flmn of dimension {flmn_3d.shape} to 1D indexing"
        )

    for n in range(-N + 1, N):
        for el in range(L):
            for m in range(-el, el + 1):
                flmn_1d[elmn2ind(el, m, n, L, N)] = flmn_3d[el, L - 1 + m, N - 1 + n]

    return flmn_1d


def flmn_1d_to_3d(flmn_1d: np.ndarray, L: int, N: int = 1) -> np.ndarray:
    r"""Convert from 1D indexed Wigner coefficients to 3D indexed coefficients.

    Args:
        flm_1d (np.ndarray): 1D indexed Wigner coefficients, C flatten index priority
            :math:`n, \ell, m`.

        L (int): Harmonic band-limit.

        N (int, optional): Number of Fourier coefficients for tangent plane rotations
            (i.e. directionality). Defaults to 1.

    Raises:
        ValueError: `flmn` is already 3D indexed.

        ValueError: `flmn` is not 1D.

    Returns:
        np.ndarray: 3D indexed Wigner coefficients, index order :math:`[\ell, m, n]`.
    """
    flmn_3d = np.zeros(flmn_shape(L, N), dtype=np.complex128)

    if len(flmn_1d.shape) == 3:
        raise ValueError(f"Flmn is already 3D indexed")
    elif len(flmn_1d.shape) != 1:
        raise ValueError(
            f"Cannot convert flmn of dimension {flmn_1d.shape} to 3D indexing"
        )

    for n in range(-N + 1, N):
        for el in range(L):
            for m in range(-el, el + 1):
                flmn_3d[el, L - 1 + m, N - 1 + n] = flmn_1d[elmn2ind(el, m, n, L, N)]

    return flmn_3d
