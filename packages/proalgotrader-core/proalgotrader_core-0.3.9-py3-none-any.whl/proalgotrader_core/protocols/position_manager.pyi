import abc
from abc import ABC, abstractmethod
from proalgotrader_core.algorithm import Algorithm as Algorithm
from proalgotrader_core.position import Position as Position

class PositionManagerProtocol(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, algorithm: Algorithm): ...
    @abstractmethod
    async def initialize(self, position: Position) -> None: ...
    @abstractmethod
    async def next(self) -> None: ...
