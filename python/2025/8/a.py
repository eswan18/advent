import math
from typing import Self
from dataclasses import dataclass
from itertools import combinations
import heapq

# 10 for testing; 1000 for real.
N_CONNECTIONS = 1000

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        x, y, z = line.strip().split(',')
        return cls(x=int(x), y=int(y), z=int(z))
    
    def distance_from(self, pt: Self) -> float:
        return math.sqrt(
            ((self.x - pt.x) ** 2)
            + ((self.y - pt.y) ** 2)
            + ((self.z - pt.z) ** 2)
        )
    

@dataclass(frozen=True)
class Box:
    id: int
    pt: Point


def a(input: str) -> str:
    points = [Point.from_line(line) for line in input.splitlines()]
    boxes = [Box(id=idx, pt=pt) for (idx, pt) in enumerate(points)]
    n_boxes = len(boxes)
    # Find the distances between all possible pairs of boxes, keeping them in a heap
    distances: list[tuple[float, tuple[int, int]]] = []
    for i, j in combinations(range(n_boxes), 2):
        element = (boxes[i].pt.distance_from(boxes[j].pt), (i, j))
        heapq.heappush(distances, element)
    
    # A mapping from a box number to its cluster number, for boxes in a cluster
    clusters: dict[int, int] = {}

    for _ in range(N_CONNECTIONS):
        _distance, (i, j) = heapq.heappop(distances)
        # "Join" these boxes. There are a few scenarios.
        if i in clusters and j not in clusters:
            # Add j to the same cluster as i
            clusters[j] = clusters[i]
        elif j in clusters and i not in clusters:
            # Add i to the same cluster as j
            clusters[i] = clusters[j]

        elif i not in clusters and j not in clusters:
            # If neither is in a cluster, we make a new cluster!
            if len(clusters) > 0:
                new_cluster_num = max(clusters.values()) + 1
            else:
                new_cluster_num = 0
            clusters[i] = new_cluster_num
            clusters[j] = new_cluster_num
        
        else:
            # The tricky case: i & j are already in different clusters.
            # We'll identify j's cluster and move it into i's.
            merged_from = clusters[j]
            merged_into = clusters[i]
            for box_id in clusters:
                if clusters[box_id] == merged_from:
                    clusters[box_id] = merged_into

    # Reorganize these into groups.
    cluster_boxes: dict[int, list[int]] = {}
    for box_id, cluster_num in clusters.items():
        if cluster_num not in cluster_boxes:
            cluster_boxes[cluster_num] = [box_id]
        else:
            cluster_boxes[cluster_num].append(box_id)
    
    cluster_sizes = [len(box_ids) for box_ids in cluster_boxes.values()]
    # Get the top 3 cluster sizes.
    cluster_sizes = sorted(cluster_sizes, reverse=True)

    result = cluster_sizes[0] * cluster_sizes[1] * cluster_sizes[2]
    return str(result)