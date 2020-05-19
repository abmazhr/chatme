from src.application.types import NamedTuple, Enum


class Status(Enum):
    HEALTHY = 0
    UNHEALTHY = 1


class HealthCheckStatus(NamedTuple):
    service_name: str
    service_state: Status
