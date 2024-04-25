from abc import ABC, abstractmethod

from ..model import Response, Query, Protocol


class BaseProtocol(ABC):
    @abstractmethod
    def connect(self, protocol: Protocol) -> None:
        raise NotImplementedError('Метод connect не реализован')

    @abstractmethod
    def execute(self, query: Query) -> Response:
        raise NotImplementedError('Метод execute не реализован')

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError('Метод close не реализован')
