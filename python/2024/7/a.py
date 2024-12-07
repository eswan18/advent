from .equation import Equation

def a(input: str) -> str:
    eqs = [Equation.from_str(s) for s in input.splitlines()]
    solvable_eqs = [eq for eq in eqs if eq.has_solution()]
    return str(sum(eq.result for eq in solvable_eqs))