from datetime import datetime
import logging
import sys
import time
from iqrfpy.messages import (
    IRequest,
    IResponse,
    FrcSendReq,
    FrcSendRsp,
    FrcSendSelectiveReq,
    FrcSendSelectiveRsp,
    FrcExtraResultReq,
    FrcExtraResultRsp,
)
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import BROADCAST_ADDR, IQMESH_TEMP_ADDR, ResponseCodes, COORDINATOR_NADR, NODE_NADR_MAX

from .iqmesh_ntw import IqmeshNtw
from .objects import GatewayParams, TransportType
from .utils import StringFormatter, PrintUtils

try:
    import iqrfide
except:
    pass


class IqrfApplication:
    """Application class for interacting with IQRF devices and networks using various transport methods."""

    def __init__(self):

        self._app_start_time = None
        self._running_under_iqrfide = None
        self._transport = None
        self._current_transport = None
        self._mqtt_response_time = None
        self._response_code = None
        self.ntw = IqmeshNtw()

        # Logger settings
        self.default_log_level = logging.DEBUG

        self.logger = logging.getLogger()
        self.logger.setLevel(level=self.default_log_level)
        self.logger.addHandler(hdlr=logging.StreamHandler(stream=sys.stdout))

    @property
    def running_under_iqrfide(self):
        """Property to check if the application is running under IQRF IDE.

        Returns:
            bool: True if running under IQRF IDE, False otherwise.
        """
        return self._running_under_iqrfide

    @property
    def current_transport(self):
        """Property to get the current transport type.

        Returns:
            str: The current transport type (e.g., IQRF IDE, MQTT).
        """
        return self._current_transport

    @property
    def response_code(self):
        """Property to get the last response code received.

        Returns:
            int: The last response code received from IQRF device.
        """
        return self._response_code

    def start(self):
        """Starts the application and logs the start time."""
        self._app_start_time = datetime.now()
        PrintUtils.print_timestamp_pair('### Start ###', self._app_start_time)

    def clean_up(self):
        """Cleans up resources if possible."""
        try:
            self._transport.terminate()
        except:  # TODO: specific exceptions
            pass

    def abort(self, message: str):
        """Aborts the application, logs the message and performs cleanup.

        Args:
            message (str): The error message to log.
        """
        print(f'\n{message}')
        PrintUtils.print_timestamp_pair('### Script aborted ###')
        self.clean_up()
        exit()

    def end(self):
        """Ends the application, logs the end time and duration, and performs cleanup."""
        app_end_time = datetime.now()
        exec_time = str(app_end_time - self._app_start_time)[:-3]
        PrintUtils.print_pair(
            '### End ###',
            f'{StringFormatter.format_time(app_end_time)} (duration: {exec_time})'
        )
        self.clean_up()

    def connect(self, transport_type: TransportType = TransportType.IQRF_IDE, gw_params: GatewayParams | None = None):
        """Connects the application to the specified transport method (e.g., IQRF IDE, MQTT) and logs result.

        Args:
            transport_type (TransportType): The transport method to use (default is IQRF IDE).
            gw_params (dict, optional): IQRF gateway configuration (required for MQTT only).

        Raises:
            ImportError: If the specified transport is not available.
        """
        self._current_transport = transport_type
        # IQRF IDE detection
        try:
            import __main__
            self._running_under_iqrfide = __main__.IQRFIDE
        except:
            self._running_under_iqrfide = False

        if self._current_transport == TransportType.IQRF_IDE:
            # Transport IQRF IDE
            try:
                from iqrfpy.ext.iqrfide_transport import IqrfIdeTransport
            except:
                print('\nThe IQRF_IDE transport can be used in the IQRF IDE only')
                exit()
        else:
            # Transport MQTT
            from iqrfpy.ext.mqtt_transport import MqttTransportParams, MqttTransport
            # Treatment of functions extended in IQRF IDE
            if not self._running_under_iqrfide:
                time.sleep_ide = time.sleep

            if gw_params is None:
                print('MQTT transport requires gw_params.')
                exit()

            # MQTT transport configuration
            gw_id = gw_params.gw_id
            self._mqtt_response_time = gw_params.mqtt_rsp_time
            mqtt_params = MqttTransportParams(
                host=gw_params.address,
                port=1883,
                client_id=gw_params.mqtt_client_id,
                user=gw_params.mqtt_user,
                password=gw_params.mqtt_password,
                request_topic=f'gateway/{gw_id.lower()}/iqrf/requests',
                response_topic=f'gateway/{gw_id.lower()}/iqrf/responses',
                qos=1,
                keepalive=25
            )

        PrintUtils.print_pair('Transport:', self._current_transport)

        try:
            if self._current_transport == TransportType.IQRF_IDE:
                self._transport = IqrfIdeTransport()
                PrintUtils.print_pair('IQRF IDE version:', iqrfide.__version__)
                # Enable logging to the IQRF IDE Terminal Log
                self._transport.iqrfide_logging = True
            else:
                self._transport = MqttTransport(params=mqtt_params, auto_init=True)
        except Exception as e:
            self.abort(f'Connection error: {str(e)}')

        PrintUtils.print_timestamp_pair('Connected:')

    def dpa_send_receive(self, request: IRequest, log_level: int = logging.ERROR) -> IResponse:
        """Sends a DPA request, receives a response, and logs the communication details (according to the specified level).

        Args:
            request (IRequest): The DPA request to send.
            log_level (int, optional): The level of details in the log (default is logging.ERROR).
                logging.ERROR: Only errors reported
                logging.INFO: Timestamps, NADRs and errors reported
                logging.DEBUG: Everything reported

        Returns:
            IResponse: The DPA response received, or None if there was no response or if the response code is not ResponseCodes.OK.
        """
        self._response_code = None
        current_log_level = self.logger.level
        self.logger.setLevel(log_level)
        request_nadr = request.nadr
        dpa_rsp_time = request.dpa_rsp_time
        dev_process_time = request.dev_process_time

        self.logger.info(StringFormatter.format_pair('NADR:', request_nadr))
        self.logger.info(StringFormatter.format_pair('Request sent:', StringFormatter.format_time(datetime.now())))
        # DPA request as bytes
        req_as_bytes = request.to_dpa()
        req_as_bytes = ' '.join("{:02X}".format(req_byte) for req_byte in req_as_bytes)
        self.logger.debug(StringFormatter.format_pair('DPA request:', req_as_bytes))

        self.logger.debug(StringFormatter.format_pair('DPA timeout:', f'{dpa_rsp_time} s'))
        self.logger.debug(StringFormatter.format_pair('DPA process time:', f'{dev_process_time} s'))
        if self._current_transport == TransportType.MQTT:
            mqtt_rsp_time = self._mqtt_response_time

            # Calculate DPA response time if not specified
            if dpa_rsp_time is None:
                dpa_rsp_time = self.ntw.get_routing_time(request_nadr)

            # Set MQTT transport timeout: must be longer than DPA timeout
            mqtt_rsp_time += (dpa_rsp_time + (dev_process_time if dev_process_time is not None else 0))
            self.logger.debug(StringFormatter.format_pair('Transport timeout:', f'{mqtt_rsp_time} s'))

        try:
            # Send/receive according to the transport
            if self._current_transport == TransportType.MQTT:
                received_response = self._transport.send_and_receive(request, mqtt_rsp_time)
            else:
                received_response = self._transport.send_and_receive(request)
        except Exception as e:
            self.logger.error(StringFormatter.format_pair(f'Error (NADR {request_nadr}):', str(e)))
        else:
            # Request to broadcast (0xFF) or temporary (0xFE) address returns no response (received_response = None)
            if (request_nadr == BROADCAST_ADDR) or (request_nadr == IQMESH_TEMP_ADDR):
                self.logger.info(StringFormatter.format_pair('No response:', 'broadcast or temporary address'))
                return received_response

            self.logger.info(
                StringFormatter.format_pair(
                    'Response received:',
                    StringFormatter.format_time(datetime.now())
                )
            )
            self._response_code = received_response.rcode
            # Report when there is an error or always at DEBUG level
            if not (ResponseCodes.is_ok_response(self._response_code)) or self.logger.level == logging.DEBUG:
                self.logger.error(
                    StringFormatter.format_pair(
                        f'Rsp code (NADR {request_nadr}):',
                        f'{self._response_code}: {ResponseCodes.to_string(self._response_code)}'
                    )
                )

            if self._current_transport == TransportType.MQTT:
                self.logger.debug(StringFormatter.format_pair('Message type:', received_response.mtype))
                self.logger.debug(StringFormatter.format_pair('Message ID:', received_response.msgid))
            self.logger.debug(
                StringFormatter.format_pair(
                    'PDATA:',
                    Common.list_to_hex_string(received_response.pdata, separator='.', uppercase=True) if
                    received_response.pdata is not None else 'No PDATA.')
            )

            if not ResponseCodes.is_ok_response(self._response_code):
                received_response = None
            return received_response
        finally:
            self.logger.info('------')
            self.logger.setLevel(current_log_level)

    def frc_send_receive(self, frc_cmd: int, user_data: list[int], selected_nodes: list[int] = None) -> dict:
        """Sends (Selective) FRC and Extra Result requests, receives responses, and logs possible errors.

        Args:
            frc_cmd (int): FRC command to send.
            user_data (list[int]): FRC user data to send.
            selected_nodes (list[int], optional): List of Node addresses to which the FRC should be sent
                selectively (default is None - non-selective FRC).

        Returns:
            dict: A dictionary containing the received response data.
                Keys:
                    - 'frc_complete' (bool): Indicates if the FRC operation is complete
                        (both FRC Send and Extra Result responses are received without error).
                    - 'frc_status' (int): FRC Status code.
                    - 'frc_data' (bytes): FRC data.
                    - 'frc_extra_result' (bytes): FRC extra result data.
        """
        rsp_data = {"frc_complete": False, "frc_status": None, "frc_data": None, "frc_extra_result": None}
        # Send/receive FRC or Selective FRC
        if selected_nodes is None:
            response: FrcSendRsp = self.dpa_send_receive(FrcSendReq(COORDINATOR_NADR, frc_cmd, user_data))
        else:
            response: FrcSendSelectiveRsp = self.dpa_send_receive(
                FrcSendSelectiveReq(COORDINATOR_NADR, frc_cmd, selected_nodes, user_data)
            )

        if response:
            err_txt = None
            frc_status = response.status
            rsp_data["frc_status"] = frc_status
            # Check FRC Status according to the IQRF OS Ref. Guide
            if frc_status > NODE_NADR_MAX:
                if frc_status == 0xFF:
                    err_txt = f'No Node is bonded'
                else:
                    err_txt = f'FRC error'
            else:
                # FRC status OK or No Node responded
                rsp_data["frc_data"] = response.frc_data
                # Send/receive FRC Extra Result
                response: FrcExtraResultRsp = self.dpa_send_receive(FrcExtraResultReq(COORDINATOR_NADR))
                if response:
                    # FRC data is complete
                    rsp_data["frc_extra_result"] = response.frc_data
                    rsp_data["frc_complete"] = True

            if err_txt:
                PrintUtils.print_pair('Error:', f'{err_txt} (status: 0x{frc_status:02X})')
        return rsp_data
