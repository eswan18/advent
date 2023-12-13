from .spring import SpringArrangementReading

UNFOLD_FACTOR = 5


def b(input: str) -> str:
    readings = [SpringArrangementReading.build_from_line(line) for line in input.splitlines()]
    readings = [reading.unfold(UNFOLD_FACTOR) for reading in readings]
    print(readings[0])
    arrangement_counts = [reading.arrangement_count() for reading in readings]
    return str(sum(arrangement_counts))