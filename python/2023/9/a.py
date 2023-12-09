from .history import History


def a(input: str) -> str:
    histories = [History.build_from_line(line) for line in input.splitlines()]
    sum_of_next = sum(history.find_next() for history in histories)
    return str(sum_of_next)