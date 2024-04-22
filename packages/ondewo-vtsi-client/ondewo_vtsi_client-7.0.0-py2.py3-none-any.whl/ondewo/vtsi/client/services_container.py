from dataclasses import dataclass

from ondewo.utils.base_service_container import BaseServicesContainer

from ondewo.vtsi.client.services.calls import Calls
from ondewo.vtsi.client.services.projects import Projects


@dataclass
class ServicesContainer(BaseServicesContainer):
    projects: Projects
    calls: Calls
