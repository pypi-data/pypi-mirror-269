"""IQMESH network class."""

from typing import List

from iqrfpy.utils.dpa import (
    COORDINATOR_NADR,
    BROADCAST_ADDR,
    IQMESH_TEMP_ADDR,
    LOCAL_DEVICE_ADDR,
)

from .ntw_device import NtwDevice

__all__ = (
    'IqmeshNtw'
)


class IqmeshNtw(object):
    """A class representing an IQMESH network."""

    __slots__ = 'coordinator', 'bonded_nodes', 'discovered_nodes'

    def __init__(self, coordinator: NtwDevice | None = None, bonded_nodes: List[int] | None = None,
                 discovered_nodes: List[int] | None = None):
        """IQMESH network constructor.

        Args:
            coordinator (NtwDevice, optional): Coordinator device. Defaults to None.
            bonded_nodes (List[int], optional): List of bonded node addresses.
                If unspecified, initialized to [].
            discovered_nodes (List[int], optional): List of discovered node addresses.
                If unspecified, initialized to [].
        """
        self.coordinator: NtwDevice | None = coordinator
        """Coordinator device."""
        self.bonded_nodes: List[int] = bonded_nodes or []
        """List of bonded node addresses."""
        self.discovered_nodes: List[int] = discovered_nodes or []
        """List of discovered node addresses."""

    def get_node_count(self) -> int:
        """Get the number of bonded nodes in the network.

        Returns:
            int: The number of bonded Nodes.
        """
        return len(self.bonded_nodes)

    def get_discovered_count(self) -> int:
        """Get the number of discovered nodes in the network.

        Returns:
            int: The number of discovered Nodes.
        """
        return len(self.discovered_nodes)

    def is_bonded(self, nadr: int) -> bool:
        """Check if a node with a given address is bonded to the network.

        Args:
            nadr (int): The address of the Node to check.

        Returns:
            bool: True if the node is bonded, False otherwise.
        """
        return nadr in self.bonded_nodes

    def validate_nadr(self, nadr: int) -> bool:
        """Validate a node address (NADR) for an IQMESH network.

        This function checks if a given node address (NADR) is valid within an IQMESH network. A valid NADR can
        either be bonded to the network or match certain predefined values such as coordinator, broadcast,
        temporary IQMESH address, or local device address.

        Args:
            nadr (int): The node address to be validated.

        Returns:
            bool: True if the NADR is valid, False otherwise.
        """
        return self.is_bonded(nadr) or nadr in [
            COORDINATOR_NADR,
            BROADCAST_ADDR,
            IQMESH_TEMP_ADDR,
            LOCAL_DEVICE_ADDR
        ]

    def get_routing_time(self, nadr: int) -> float:
        """Calculate the routing time based on the longest timeslot in a given RF mode.

        This function calculates the routing time for a specific node address by taking into account the
        safety time and whether it's a coordinator, local device, broadcast, or unicast. The routing time is
        based on the longest timeslot in the RF mode.

        Args:
            nadr (int): Node address for which the routing time is calculated.

        Returns:
            float: The calculated routing time in seconds.
        """
        safety_time = 0.1  # [s]
        if nadr == COORDINATOR_NADR or nadr == LOCAL_DEVICE_ADDR:
            routing_time = 0.5  # [s]
        else:
            routing_time = (self.get_discovered_count() + 1) * self.coordinator.longest_timeslot
            if nadr != BROADCAST_ADDR and nadr != IQMESH_TEMP_ADDR:
                # It is an unicast, so it will also route back
                routing_time *= 2
        return round(routing_time + safety_time, 2)
