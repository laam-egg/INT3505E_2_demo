import pybreaker

circuit_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=10)
