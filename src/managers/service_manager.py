from typing import Dict, Type, TypeVar

T = TypeVar('T')

class ServiceManager:
    _services: Dict[Type, object] = {}

    @classmethod
    def register(cls, service_type: Type[T], instance: T) -> None:
        cls._services[service_type] = instance

    @classmethod
    def get(cls, service_type: Type[T]) -> T:
        if service_type not in cls._services:
            raise KeyError(f"Service {service_type.__name__} not registered")
        return cls._services[service_type]
