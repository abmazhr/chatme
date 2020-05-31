from src.application.entity.service import Service
from src.application.types import (
    List,
    Dict
)


def health_check(*, services: List[Service]) -> Dict[str, str]:
    def get_service_health_status(service):
        try:
            return service.service_instance.health_check().service_state.name
        except Exception:
            return f"There is no 'health_check' function for this service " \
                   f"[{service.service_instance.__class__.__name__}]."

    return {
        service.service_instance.__class__.__name__: get_service_health_status(service)
        for service in services
    }
