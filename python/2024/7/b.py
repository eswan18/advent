from .threeway_equation import ThreewayEquation

def b(input: str) -> str:
    eqs = [ThreewayEquation.from_str(s) for s in input.splitlines()]
    solvable_eqs = [eq for eq in eqs if eq.has_solution()]
    return str(sum(eq.result for eq in solvable_eqs))