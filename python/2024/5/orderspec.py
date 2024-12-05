from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class PageOrderSpec:
    before: set[int] = field(default_factory=set)
    after: set[int] = field(default_factory=set)

@dataclass
class OrderSpec:
    pages: defaultdict[int, PageOrderSpec] = field(default_factory=lambda: defaultdict(PageOrderSpec))

    def __repr__(self) -> str:
        s = ''
        for page, spec in self.pages.items():
            s += f'{page}: {spec}\n'
        return s