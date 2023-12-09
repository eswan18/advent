from .history import History


def b(input: str) -> str:
    histories = [History.build_from_line(line) for line in input.splitlines()]
    sum_of_prev = sum(history.find_previous() for history in histories)
    return str(sum_of_prev)