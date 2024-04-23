from iqrfpy.objects import ExplorationPerEnumData, OsReadData, OsTrConfData
from iqrfpy.utils.common import Common
from iqrfpy.peripherals.exploration import PeripheralEnumerationResponse
from iqrfpy.peripherals.os import ReadTrConfResponse
from tabulate import tabulate, SEPARATING_LINE

__all__ = (
    'NtwDevice'
)


class NtwDevice(object):
    """Represents an IQRF network device and provides methods for managing and retrieving device information."""

    __slots__ = 'mid', 'os_ver', 'os_build', 'tr_type', 'supply_voltage', 'shortest_timeslot', 'longest_timeslot', \
        'tr_config_checksum', 'tr_config', 'tr_rfpgm', 'tr_init_phy', 'rf_band', 'is_thermometer', 'is_eeeprom', \
        'is_il_type', 'dpa_ver', 'hwpid', 'hwpid_ver', 'std_lp_ntw_type', 'lp_rf_mode'

    def __init__(self, data: OsReadData | None = None):
        """Network device constructor.

        Args:
            data (OsReadData, optional): Data to initialize the device instance.
        """
        self.shortest_timeslot = None
        self.longest_timeslot = None
        self.tr_config_checksum = None
        self.tr_config: OsTrConfData | None = None
        self.tr_rfpgm = None
        self.tr_init_phy = None
        self.rf_band = None
        self.is_thermometer = None
        self.is_eeeprom = None
        self.is_il_type = None
        self.dpa_ver = None
        self.hwpid = None
        self.hwpid_ver = None
        self.std_lp_ntw_type = None
        self.lp_rf_mode = None
        if data is None:
            return
        self.mid = f'{data.mid:08X}'
        major = (data.os_version & 0xF0) >> 4
        minor = data.os_version & 0x0F
        # TR type
        self.tr_type = data.tr_mcu_type.tr_series
        # OS version
        self.os_ver = f'{major}.{minor:02d}{data.tr_mcu_type.mcu_type}'
        # OS build
        self.os_build = f'{data.os_build:04X}'
        # Power supply
        self.supply_voltage = round(data.supply_voltage, 2)
        # Timeslot limits
        self.shortest_timeslot = ((data.slot_limits & 0x0F) + 3) * 0.01
        self.longest_timeslot = (((data.slot_limits & 0xF0) >> 4) + 3) * 0.01
        # Peripheral enumeration
        self._parse_peripheral_enum(data.per_enum)

    def _parse_peripheral_enum(self, data: ExplorationPerEnumData):
        """
        Saves and parses peripheral enumeration data to the object.

        Args:
          data (PeripheralEnumerationData): The peripheral enumeration data to be saved.
        """
        self.dpa_ver = data.dpa_version
        self.hwpid = data.hwpid
        self.hwpid_ver = data.hwpid_ver
        self.std_lp_ntw_type = bool(data.flags & 0x04)
        self.lp_rf_mode = bool(data.flags & 0x02)

    def device_ident_str(self) -> str:
        """
        Returns a formatted string representing the TR module information.

        Returns:
            str: A string containing the TR module type, MID, IQRF OS version, and build number.
        """
        ident_headers = ['Device identification', '']
        ident_data = [
            ['TR series', self.tr_type],
            ['MID', self.mid],
            ['IQRF OS', f'{self.os_ver} ({self.os_build})'],
            ['DPA', Common.dpa_version_to_str(self.dpa_ver)],
            ['HWPID', f'0x{self.hwpid:04X} (ver: {int(self.hwpid_ver / 256):02X}.{(self.hwpid_ver & 0x00FF):02X})'],
            ['Network type', 'STD+LP' if self.std_lp_ntw_type else 'STD'],
            ['RF mode', 'LP' if self.lp_rf_mode else 'STD'],
        ]
        return tabulate(headers=ident_headers, tabular_data=ident_data, tablefmt='double_outline')

    def set_peripheral_enum(self, data: PeripheralEnumerationResponse):
        self._parse_peripheral_enum(data.per_enum_data)

    def set_tr_conf(self, data: ReadTrConfResponse) -> bool:
        """
        Saves and parses TR configuration from Read TR configuration response to the object.

        Args:
            data (ReadTrConfResponse): Read TR configuration response.

        Returns:
            bool: True if the checksum of the TR configuration is valid, False otherwise.
        """
        # Check the checksum from the "Configuration" part of PDATA
        if data.checksum != OsTrConfData.calculate_checksum(data.configuration.to_pdata()):
            return False
        self.tr_config_checksum = data.checksum
        self.tr_config = data.configuration
        self.tr_rfpgm = data.rfpgm
        self.tr_init_phy = data.init_phy.value
        self.rf_band = data.init_phy.rf_band
        self.is_thermometer = data.init_phy.thermometer_present
        self.is_eeeprom = data.init_phy.serial_eeprom_present
        self.is_il_type = data.init_phy.il_type
        return True

    def is_per_enabled(self, per: int) -> bool:
        """
        Checks if a specific peripheral in the TR configuration is enabled.

        Args:
            per (int): The peripheral to check.

        Returns:
            bool: True if the peripheral is enabled, False otherwise.
        """
        return per in self.tr_config.embedded_peripherals

    def tr_conf_str(self):
        """
        Returns a formatted string representing the TR configuration.

        Returns:
            str: A string containing TR configuration parameters.
        """
        init_phy_headers = ['Init PHY', '']
        init_phy_data = [
            ['RF Band', str(self.rf_band)],
            ['Thermometer', str(self.is_thermometer)],
            ['EEEPROM', str(self.is_eeeprom)],
            ['IL', str(self.is_il_type)],
        ]
        rf_headers = ['RF', '']
        rf_data = [
            ['Network type', 'STD+LP' if self.tr_config.std_and_lp_network else 'STD'],
            ['TX power', self.tr_config.rf_output_power],
            ['RX filter', self.tr_config.rf_signal_filter],
            ['LP RX timeout', self.tr_config.lp_rf_timeout],
            ['Channel A', self.tr_config.rf_channel_a],
            ['Channel B', self.tr_config.rf_channel_b],
            ['Alternative DSM channel', self.tr_config.alternative_dsm_channel],
        ]
        embedded_pers_headers = ['Embedded peripherals (enabled)']
        embedded_pers_data = [[str(x.name)] for x in self.tr_config.embedded_peripherals]
        other_headers = ['Other', '']
        other_data = [
            ['Custom DPA handler', str(self.tr_config.custom_dpa_handler)],
            ['DPA Peer-to-Peer', str(self.tr_config.dpa_peer_to_peer)],
            ['User Peer-to-Peer', str(self.tr_config.user_peer_to_peer)],
            ['Local FRC', str(self.tr_config.local_frc)],
            ['IO Setup', str(self.tr_config.io_setup)],
            ['Routing off', str(self.tr_config.routing_off)],
            ['Stay awake when not bonded', str(self.tr_config.stay_awake_when_not_bonded)],
        ]
        init_phy_str = tabulate(headers=init_phy_headers, tabular_data=init_phy_data, tablefmt='double_outline')
        rf_str = tabulate(headers=rf_headers, tabular_data=rf_data, tablefmt='double_outline')
        embedded_pers_str = tabulate(headers=embedded_pers_headers, tabular_data=embedded_pers_data,
                                     tablefmt='double_outline')
        other_str = tabulate(headers=other_headers, tabular_data=other_data, tablefmt='double_outline')
        return '\n'.join([init_phy_str, rf_str, embedded_pers_str, other_str])
