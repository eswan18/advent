from collections import defaultdict
from dataclasses import dataclass, field

type Node = str
type Path = tuple[Node, Node]

@dataclass
class NodeVisitor:
    paths: dict[Node, list[Node]]
    visited: set = field(default_factory=set)

    def find_reachable_nodes(self, start: Node) -> set[Node]:
        self._find_reachable_nodes(start)
        return self.visited

    def _find_reachable_nodes(self, start: Node):
        self.visited.add(start)
        children = self.paths.get(start, [])
        unvisited = [c for c in children if c not in self.visited]
        for node in unvisited:
            self.find_reachable_nodes(node)


def build_path_mapping(p: list[Path]) -> dict[Node, list[Node]]:
    d = defaultdict(list)
    for src, dest in p:
        d[src].append(dest)
    return dict(d)
    

def build_reverse_path_mapping(p: list[Path], exclude: set[Node]) -> dict[Node, list[Node]]:
    d = defaultdict(list)
    for src, dest in p:
        if src in exclude or dest in exclude:
            continue
        d[dest].append(src)
    return dict(d)

def traverse(m: dict[Node, list[Node]], start: str, end: str) -> int:
    if start == end:
        return 1
    return sum(traverse(m, node, end) for node in m.get(start, []))


def a(input: str) -> str:
    connections: list[Path] = []
    for line in input.splitlines():
        src, rest = line.split(': ')
        dests = rest.strip().split(' ')
        for d in dests:
            connections.append((src, d))
    forward_map = build_path_mapping(connections)
    reachable = NodeVisitor(forward_map).find_reachable_nodes('you')
    # Figure out what nodes aren't reachable from the start node.
    unreachable = forward_map.keys() - reachable

    reverse_map = build_reverse_path_mapping(connections, exclude=unreachable)
    return str(traverse(reverse_map, 'out', 'you'))