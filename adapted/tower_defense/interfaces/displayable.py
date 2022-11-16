from abc import abstractmethod, ABC


class IDisplayable(ABC):
    @abstractmethod
    def get_model_name(self) -> str:
        ...
