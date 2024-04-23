"""Application helpers objects, enums and data classes."""

from dataclasses import dataclass
from enum import IntEnum

__all__ = (
    'GatewayParams',
    'TransportType'
)


@dataclass
class GatewayParams:
    """Gateway parameters class.

    This data class holds parameters for communication with IQRF Gateway using the MQTT transport,
    and is used by the IqrfApplication class.
    """

    __slots__ = 'address', 'gw_id', 'mqtt_user', 'mqtt_password', 'mqtt_rsp_time', 'mqtt_client_id'

    def __init__(self, address: str, gw_id: str, mqtt_user: str, mqtt_password: str, mqtt_rsp_time: int,
                 mqtt_client_id: str | None = None):
        """Gateway parameters constructor.

        Args:
            address (str): Gateway address, IP address or FQDN.
            gw_id (str): Gateway ID.
            mqtt_user (str): MQTT broker username.
            mqtt_password (str): MQTT broker password.
            mqtt_rsp_time (int): MQTT response timeout in seconds.
            mqtt_client_id (str, optional): MQTT Client ID. If unspecified, a random client ID is generated.
                Defaults to None.
        """
        self.address: str = address
        """Gateway IP or FQDN."""
        self.gw_id: str = gw_id
        """Gateway ID."""
        self.mqtt_user: str = mqtt_user
        """MQTT broker username."""
        self.mqtt_password: str = mqtt_password
        """MQTT broker password."""
        self.mqtt_rsp_time: int = mqtt_rsp_time
        """MQTT response timeout in seconds."""
        self.mqtt_client_id: str | None = mqtt_client_id
        """MQTT Client ID."""


class TransportType(IntEnum):
    """Transport types enum class."""
    MQTT = 0
    IQRF_IDE = 1

    def __str__(self):
        """String representation of transport type.

        Implementation overrides default str() behavior.

        Returns:
            str: Human-readable transport type string.
        """
        return self.name.replace('_', ' ')
