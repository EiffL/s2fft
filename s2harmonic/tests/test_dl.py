import s2harmonic as s2h
import pytest
import numpy as np
import pyssht as ssht


def test_trapani():
    """Test Trapani recursions"""

    # Test all dl(pi/2) terms up to L.
    L = 5

    # Compute using SSHT.
    beta = np.pi / 2.0
    dl_array = ssht.generate_dl(beta, L)

    # Compare to routines in SSHT, which have been validated extensively.
    dl = np.zeros((2 * L - 1, 2 * L - 1))
    for el in range(L):
        dl = s2h.dl.trapani_full(dl, L, el)
        np.testing.assert_allclose(dl_array[el, :, :], dl, atol=1e-15)
