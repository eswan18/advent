from dataclasses import dataclass

@dataclass
class History:
    values: list[int]

    @classmethod
    def build_from_line(cls, line: str):
        values = [int(value) for value in line.split(' ')]
        return cls(values)
    
    def find_next(self) -> int:
        delta_lines = []
        deltas = self.values
        # Build out the deltas until they are all equal (the step before they're all 0).
        while True:
            deltas = [deltas[i] - deltas[i-1] for i in range(1, len(deltas))]
            delta_lines.append(deltas)
            deltas_are_all_equal = len(set(deltas)) == 1
            if deltas_are_all_equal:
                break
        # Now work backwards to find the next value for each list of deltas.
        while len(delta_lines) > 1:
            deltas = delta_lines.pop()
            # solve such that the next value of the previous deltas is offset from the previous by the last current delta.
            next_value = delta_lines[-1][-1] + deltas[-1]
            delta_lines[-1].append(next_value)
        # Now we have just one list of deltas, and we can apply it to the main values sequence.
        return self.values[-1] + delta_lines[0][-1]

    def __str__(self):
        return ' '.join(str(value) for value in self.values)