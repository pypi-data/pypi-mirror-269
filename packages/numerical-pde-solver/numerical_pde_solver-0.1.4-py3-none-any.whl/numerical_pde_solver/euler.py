import numpy as np

def euler_method(f, g, x0, t0, T, dt):
    """
    Approximate the solution of the stochastic differential equation:
    dx = f(x, t) dt + g(x, t) dW, via the Euler-Maruyama method.

    Parameters:
    - f: Callable[[float, float], float]
        The drift coefficient function of the SDE, taking current state and time.
    - g: Callable[[float, float], float]
        The diffusion coefficient function of the SDE, taking current state and time.
    - x0: float
        Initial state of the process at time t0.
    - t0: float
        Starting time of the simulation.
    - T: float
        Ending time of the simulation.
    - dt: float
        Time step size.

    Returns:
    - t: numpy.ndarray
        Array of time points.
    - x: numpy.ndarray
        Array of state values at each time point.
    """
    N = int((T - t0) / dt)
    t = np.linspace(t0, T, N + 1)
    x = np.zeros(N + 1)
    x[0] = x0

    for i in range(1, N + 1):
        xi = x[i - 1]
        ti = t[i - 1]
        x[i] = xi + f(xi, ti) * dt + g(xi, ti) * np.sqrt(dt) * np.random.normal()

    return t, x
