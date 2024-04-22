from ondewo.utils.base_client import BaseClient
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.vtsi.client.services.calls import Calls
from ondewo.vtsi.client.services.projects import Projects
from ondewo.vtsi.client.services_container import ServicesContainer


class Client(BaseClient):
    """
    The core python client for interacting with ONDEWO VTSI services.
    """

    def _initialize_services(self, config: BaseClientConfig, use_secure_channel: bool) -> None:
        self.services: ServicesContainer = ServicesContainer(
            projects=Projects(config=config, use_secure_channel=use_secure_channel),
            calls=Calls(config=config, use_secure_channel=use_secure_channel),
        )
