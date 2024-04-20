
import unittest
import numpy as np
from numerical_pde_solver.milstein import milstein_method

class TestMilsteinMethod(unittest.TestCase):

    def test_linear_growth(self):
        """Test the Milstein method on dx = 3*dt + 4*dW with dW^2 term approximation."""
        def f(x, t):
            return 3

        def g(x, t):
            return 4

        def dg(x, t):
            return 0  # Derivative of g with respect to x is zero

        x0, t0, T, dt = 0, 0, 1, 0.01
        t, x = milstein_method(f, g, dg, x0, t0, T, dt)
        # Check final value is within a reasonable range
        expected_final = 3 * T + 4 * np.sqrt(T) * np.random.normal()
        np.testing.assert_allclose(x[-1], expected_final, atol=10)

    def test_zero_drift_diffusion(self):
        """Test the Milstein method on dx = 0, x(0) = 0."""
        def f(x, t):
            return 0

        def g(x, t):
            return 0

        def dg(x, t):
            return 0

        x0, t0, T, dt = 0, 0, 1, 0.01
        t, x = milstein_method(f, g, dg, x0, t0, T, dt)
        # Expect no change in x over time
        np.testing.assert_array_equal(x, np.zeros_like(x))

if __name__ == "__main__":
    unittest.main()
