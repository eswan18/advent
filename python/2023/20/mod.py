from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NamedTuple


class Signal(NamedTuple):
    high: bool
    from_name: str
    to_name: str

    def __repr__(self) -> str:
        return f"Signal({'HIGH' if self.high else 'LOW'}, {self.from_name} -> {self.to_name})"


class Module(ABC):

    def __init__(self, name: str, destinations: list[str]):
        self.name = name
        self.destinations = destinations
        self.low_pulses_sent = 0
        self.high_pulses_sent = 0
    
    @staticmethod
    def build_from_line(line: str):
        """
        Build a module from a line of input.
        """
        kind = Broadcaster
        match line[0]:
            case "%":
                kind = FlipFlopModule
                line = line[1:]
            case "&":
                kind = InvertModule
                line = line[1:]
        name, destination_str = line.split(' -> ')
        destinations = destination_str.split(', ')
        return kind(name, destinations)

    @abstractmethod
    def receive(self, signal: Signal) -> list[Signal]:
        """
        Receive a signal from a source module.
        
        Returns a list of tuples, each indicating a signal to be sent onward, in the
        form (destination_name, signal).
        """
        raise NotImplementedError
    
    def _send(self, high: bool) -> list[Signal]:
        """
        Create signals  to be sent to all destinations.

        Signals are tuples of (destination_name, signal).
        """
        if high:
            self.high_pulses_sent += len(self.destinations)
        else:
            self.low_pulses_sent += len(self.destinations)
        signals = [Signal(high, self.name, destination) for destination in self.destinations]
        return signals


class Broadcaster(Module):

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
    
    def receive(self, signal: Signal) -> list[Signal]:
        return self._send(signal.high)
    

class FlipFlopModule(Module):

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.on = False
    
    def receive(self, signal: Signal) -> list[Signal]:
        if signal.high:
            return []
        else:
            self.on = not self.on
            return self._send(self.on)
    
    def __repr__(self) -> str:
        return f"FlipFlopModule({self.name}, {self.destinations}, on={self.on})"


class InvertModule(Module):

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.inputs: dict[str, bool] = {}
    
    def receive(self, signal: Signal) -> list[Signal]:
        if len(self.inputs) == 0:
            raise RuntimeError("Inputs must be set before receiving signals.")

        self.inputs[signal.from_name] = signal.high
        if all(self.inputs.values()):
            return self._send(False)
        else:
            return self._send(True)
    
    def add_input(self, name: str):
        self.inputs[name] = False
    
    def __repr__(self) -> str:
        return f"InvertModule({self.name}, {self.destinations}, inputs={self.inputs})"


@dataclass
class ModuleSet:
    broadcaster: Broadcaster
    modules: dict[str, Module]
    low_signals_sent: int = 0
    high_signals_sent: int = 0
    button_presses: int = 0

    @classmethod
    def build_from_str(cls, s: str) -> 'ModuleSet':
        lines = s.splitlines()
        modules = [Module.build_from_line(line) for line in lines]
        # Find the broadcaster and non-broadcaster modules.
        broadcaster = [module for module in modules if isinstance(module, Broadcaster)][0]
        other_modules = [module for module in modules if not isinstance(module, Broadcaster)]

        # One last thing: InvertModules need to know their inputs. Figure those out.
        inv_modules = [module for module in other_modules if isinstance(module, InvertModule)]
        for inv_module in inv_modules:
            for module in modules:
                if inv_module.name in module.destinations:
                    inv_module.add_input(module.name)
        return cls(broadcaster, {module.name: module for module in other_modules})
    
    def press_button(self):
        """
        Press the button on the broadcaster.
        """
        # Send a low signal to the broadcaster.
        self.button_presses += 1
        signals = self.broadcaster.receive(Signal(False, "", self.broadcaster.name))
        while len(signals) > 0:
            next_signals = []
            for signal in signals:
                module = self.modules.get(signal.to_name)
                if module is None:
                    continue
                new_signals = module.receive(signal)
                next_signals.extend(new_signals)
            signals = next_signals

        self.low_signals_sent = self.broadcaster.low_pulses_sent + sum(module.low_pulses_sent for module in self.modules.values()) + self.button_presses
        self.high_signals_sent = sum(module.high_pulses_sent for module in self.modules.values())