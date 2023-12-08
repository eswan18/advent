from dataclasses import dataclass
from typing import Self

@dataclass
class Race:
    time: int
    distance: int

    @classmethod
    def from_lines(cls, lines: list[str], merge: bool = False) -> list[Self]:
        time_strs = lines[0].split(": ")[1].strip().split(" ")
        dist_strs = lines[1].split(": ")[1].strip().split(" ")
        if merge:
            times = [int(''.join(time_strs))]
            distances = [int(''.join(dist_strs))]
        else:
            times = [int(time_str) for time_str in time_strs if time_str != ""]
            distances = [int(dist_str) for dist_str in dist_strs if dist_str != ""]
        return [cls(time, distance) for time, distance in zip(times, distances)]
    
    def ways_to_win(self) -> int:
        ways = 0
        found_way = False
        for speed in range(1, self.distance - 1):
            time_remaining = self.time - speed
            if time_remaining * speed > self.distance:
                found_way = True
                ways += 1
            else:
                # If we've had some wins already but then failed, no future inputs will work.
                if found_way:
                    break
        return ways