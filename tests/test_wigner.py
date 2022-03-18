import pytest
import numpy as np
import s2harmonic.wigner as wigner
import pyssht as ssht


def test_trapani_with_ssht():
    """Test Trapani computation against ssht"""

    # Test all dl(pi/2) terms up to L.
    L = 5

    # Compute using SSHT.
    beta = np.pi / 2.0
    dl_array = ssht.generate_dl(beta, L)

    # Compare to routines in SSHT, which have been validated extensively.
    dl = np.zeros((2 * L - 1, 2 * L - 1), dtype=np.float64)
    dl = wigner.trapani.init(dl, L)
    for el in range(1, L):
        dl = wigner.trapani.compute_full(dl, L, el)
        np.testing.assert_allclose(dl_array[el, :, :], dl, atol=1e-15)


def test_trapani_vectorized():
    """Test vectorized Trapani computation"""

    # Test all dl(pi/2) terms up to L.
    L = 5

    # Compare to routines in SSHT, which have been validated extensively.
    dl = np.zeros((2 * L - 1, 2 * L - 1), dtype=np.float64)
    dl = wigner.trapani.init(dl, L)
    dl_vect = np.zeros((2 * L - 1, 2 * L - 1), dtype=np.float64)
    dl_vect = wigner.trapani.init(dl_vect, L)
    for el in range(1, L):
        dl = wigner.trapani.compute_full(dl, L, el)
        dl_vect = wigner.trapani.compute_full_vectorized(dl_vect, L, el)
        np.testing.assert_allclose(dl, dl_vect, atol=1e-15)


def test_trapani_checks():

    # TODO

    # Check throws exception if arguments wrong

    # Check throws exception if don't init

    return
