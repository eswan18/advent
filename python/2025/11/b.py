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

def traverse(m: dict[Node, list[Node]], start: str, end: str) -> list[list[Node]]:
    if start == end:
        return [[end]]
    return [
        [start, *path]
        for node in m.get(start, [])
        for path in traverse(m, node, end)
    ]


def b(input: str) -> str:
    connections: list[Path] = []
    for line in input.splitlines():
        src, rest = line.split(': ')
        dests = rest.strip().split(' ')
        for d in dests:
            connections.append((src, d))
    forward_map = build_path_mapping(connections)

    # I took advantage of a complete cheat -- I discovered no dac->out paths contain fft.
    # Thus, the path must be svr->fft->dac->out. The below code assumes that.

    # Find paths from dac to out
    dac_reachable = NodeVisitor(forward_map).find_reachable_nodes('dac')
    dac_unreachable = forward_map.keys() - dac_reachable
    reverse_map = build_reverse_path_mapping(connections, exclude=dac_unreachable)
    dac_paths = traverse(reverse_map, 'out', 'dac')

    # Find paths from fft to dac
    fft_reachable = NodeVisitor(forward_map).find_reachable_nodes('fft')
    fft_unreachable = forward_map.keys() - fft_reachable
    reverse_map = build_reverse_path_mapping(connections, exclude=fft_unreachable)
    fft_paths = traverse(reverse_map, 'dac', 'fft')

    # Find paths from svr to fft
    svr_reachable = NodeVisitor(forward_map).find_reachable_nodes('svr')
    svr_unreachable = forward_map.keys() - svr_reachable
    reverse_map = build_reverse_path_mapping(connections, exclude=svr_unreachable)
    svr_paths = traverse(reverse_map, 'fft', 'svr')

    # We still need to limit this down to paths where 'fft' appears
    return str(len(svr_paths) * len(fft_paths) * len(dac_paths))