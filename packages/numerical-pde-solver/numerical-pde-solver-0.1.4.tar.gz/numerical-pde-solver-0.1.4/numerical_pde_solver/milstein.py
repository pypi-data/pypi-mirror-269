import numpy as np

def milstein_method(f, g, dg, x0, t0, T, dt):
    """
    Approximate the solution of the stochastic differential equation:
    dx = f(x, t) dt + g(x, t) dW, via the Milstein method.

    Parameters:
    - f: Callable[[float, float], float]
        The drift coefficient function of the SDE.
    - g: Callable[[float, float], float]
        The diffusion coefficient function of the SDE.
    - dg: Callable[[float, float], float]
        The partial derivative of the diffusion coefficient with respect to the state.
    - x0: float
        Initial state of the process.
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
        dw = np.sqrt(dt) * np.random.normal()
        x[i] = xi + f(xi, ti) * dt + g(xi, ti) * dw + 0.5 * g(xi, ti) * dg(xi, ti) * (dw**2 - dt)

    return t, x
