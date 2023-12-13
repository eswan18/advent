from .spring import SpringArrangementReading, SpringArrangement, SpringStateReading, SpringState


def a(input: str) -> str:
    readings = [SpringArrangementReading.build_from_line(line) for line in input.splitlines()]
    arrangement_counts = [reading.arrangement_count() for reading in readings]
    return str(sum(arrangement_counts))