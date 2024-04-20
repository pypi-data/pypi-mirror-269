
import unittest
import numpy as np
from numerical_pde_solver.euler import euler_method

class TestEulerMethod(unittest.TestCase):

    def test_linear_growth(self):
        """Test the Euler method on dx = 5*dt + 2*dW, x(0) = 0."""
        def f(x, t):
            return 5

        def g(x, t):
            return 2

        x0, t0, T, dt = 0, 0, 1, 0.01
        t, x = euler_method(f, g, x0, t0, T, dt)
        # Check final value is within a reasonable range due to stochastic nature
        expected_final = 5 * T + 2 * np.sqrt(T) * np.random.normal()
        np.testing.assert_allclose(x[-1], expected_final, atol=5)

    def test_zero_drift_diffusion(self):
        """Test the Euler method on dx = 0, x(0) = 0."""
        def f(x, t):
            return 0

        def g(x, t):
            return 0

        x0, t0, T, dt = 0, 0, 1, 0.01
        t, x = euler_method(f, g, x0, t0, T, dt)
        # Expect no change in x over time
        np.testing.assert_array_equal(x, np.zeros_like(x))

if __name__ == "__main__":
    unittest.main()
