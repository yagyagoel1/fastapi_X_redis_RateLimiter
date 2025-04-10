from abc import ABC,abstractmethod


class  BaseRateLimiter(ABC):
    @abstractmethod
    def is_allowed(self , client_id:str)-> bool:
        pass
    